
import os
import sys

# ================= 运行时环境自动配置 =================
def _ensure_runtime():
    """自动切换至 .venv311 环境并设置 Qt 插件路径。"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    if os.name == 'nt':
        venv_python = os.path.join(project_root, '.venv311', 'Scripts', 'python.exe')
        plugin_dir = os.path.join(project_root, '.venv311', 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')
    else:
        venv_python = os.path.join(project_root, '.venv311', 'bin', 'python')
        plugin_dir = os.path.join(project_root, '.venv311', 'lib', 
                                   f'python{sys.version_info.major}.{sys.version_info.minor}', 
                                   'site-packages', 'PyQt5', 'Qt5', 'plugins')
    
    already_in_venv = (not os.path.exists(venv_python) or 
                       os.path.abspath(sys.executable) == os.path.abspath(venv_python))
    
    if already_in_venv:
        if os.path.isdir(plugin_dir) and 'QT_QPA_PLATFORM_PLUGIN_PATH' not in os.environ:
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_dir
        return
    
    if os.path.isdir(plugin_dir):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_dir
    
    os.execv(venv_python, [venv_python, os.path.abspath(__file__)] + sys.argv[1:])


def _ensure_qt_plugin_path():
    """兜底：确保 Qt 插件路径已设置。"""
    if 'QT_QPA_PLATFORM_PLUGIN_PATH' in os.environ:
        return
    
    candidates = []
    if os.name == 'nt':
        scripts_dir = os.path.dirname(sys.executable)
        candidates.append(os.path.abspath(os.path.join(scripts_dir, '..', 'Lib', 'site-packages', 
                                                        'PyQt5', 'Qt5', 'plugins')))
        project_root = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.abspath(os.path.join(project_root, '.venv311', 'Lib', 'site-packages', 
                                                        'PyQt5', 'Qt5', 'plugins')))
    else:
        lib_dir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', 'lib'))
        candidates.append(os.path.join(lib_dir, f'python{sys.version_info.major}.{sys.version_info.minor}', 
                                        'site-packages', 'PyQt5', 'Qt5', 'plugins'))
    
    for path_candidate in candidates:
        if os.path.isdir(path_candidate):
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path_candidate
            break


# 执行环境配置（必须在 import PyQt5 之前）
_ensure_runtime()
_ensure_qt_plugin_path()

# ================= 正常导入 =================
import csv
import math
from collections import defaultdict, deque
from datetime import datetime
import numpy as np
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
import pyqtgraph.opengl as gl

# 从原文件导入(如果需要)
# from escooter_plugin import EscooterPlugin, oriented_box_segments

# ================= 配置 =================

# 数据文件路径 - 【修改这里指向您的测试数据】syntropy_bike&people.csv   subtend_bike&people.csv
CSV_FILE = r'C:\Users\h\OneDrive\默认\桌面\Radar\project\Data_V3\syntropy_bike&people.csv'

# 雷达安装高度
RADAR_HEIGHT_M = 0.45

# 基础参数
ROTATE_Y_PLUS_90_FOR_X_ALIGNED_WALK = False
GRID_CELL_M = 0.5  # 【改进】从0.7减小到0.5，更精细的聚类
MIN_POINTS_IN_CLUSTER = 3
ASSOC_GATE_BASE_M = 2.0  # 【V6】基础门限2.0m
MAX_MISS = 3  # 【V6】行人快速清理3帧(0.3秒)
MAX_MISS_SR = 12  # 【V7恢复】滑板车12帧(1.2秒)，恢复V5设置，高速稀疏点云需要更长容忍

# 速度与稳定性
ROLL_WIN = 40
EWMA_ALPHA = 0.35
SPEED_WIN_PAIR = 10
SPEED_SANITY_MAX = 9.0
DISP_FACTOR = 1.25

# 行人识别参数
WALK_SPEED_LO = 0.3
WALK_SPEED_HI = 2.5
MIN_DURATION_S = 0.5
Y_EXTENT_MIN = 0.35

CONFIRM_SCORE = 3
SCORE_HIT = 2
SCORE_MISS = 1
LATCH_S = 1.0  # 【V5修复】恢复1.0秒，快速清理行人轨迹

# 绘制参数
POINT_SIZE = 3
PT_COLOR = (1, 0, 0, 1)
BOX_COLOR = (0, 1, 0, 1)
BOX_WIDTH = 2
LABEL_SPEED = True

# 方框稳定化
BOX_SIZE_MODE = 'fixed'
BOX_FIXED_WHD = (0.6, 1.7, 0.6)
BOX_SMOOTH_ALPHA = 0.25
BOX_DELTA_CLAMP = 0.12
BOX_SIZE_MIN = (0.4, 1.4, 0.4)
BOX_SIZE_MAX = (0.9, 2.0, 0.9)
BOX_ANCHOR = 'center'
BOX_PAD = 0.02
BOX_SIZE_MIN_ARR = np.array(BOX_SIZE_MIN, float)
BOX_SIZE_MAX_ARR = np.array(BOX_SIZE_MAX, float)

# ================= 【改进】滑板车识别参数 =================

# 水平尺寸 (保持不变)
SR_WIDTH_MIN = 0.25
SR_WIDTH_MAX = 1.80
SR_DEPTH_MIN = 0.25
SR_DEPTH_MAX = 1.80

# 【改进】垂直尺寸 - 提高下限避免误判行人
SR_HEIGHT_MIN = 0.50     # 从0.30提高到0.50m (行人通常<0.4m)
SR_HEIGHT_MAX = 4.00

# 点数范围
SR_POINTS_MIN = 3
SR_POINTS_MAX = 300

# 【V5修复】质心高度 - 进一步提高下限，严格区分行人
SR_CENTROID_Y_MIN = 0.90  # 【V5】从0.80提高到0.90m (行人质心<0.6m，滑板车>0.8m)
SR_CENTROID_Y_MAX = 5.00

# 速度范围
SR_SPEED_MIN = 1.5
SR_SPEED_MAX = 6.94
SR_SPEED_DANGER = 5.56
SR_MIN_DURATION_S = 0.1
SR_CONFIRM_SCORE = 1
SR_SCORE_HIT = 2
SR_SCORE_MISS = 1
SR_LATCH_S = 1.5  # 【V5修复】从2.0减少到1.5秒，加快滑板车轨迹清理

# 【新增】关联和验证参数
SR_MAX_SPEED_JUMP = 6.0      # 【改进】从4.0增加到6.0，放宽速度突变容忍
SR_MIN_SPEED_STABLE = 5      # 速度稳定性检查的最小帧数
SR_SPEED_STABLE_RATIO = 0.4  # 速度稳定性阈值(std/mean)
SR_SPARSE_FRAME_THRESHOLD = 10  # 【新增】稀疏帧阈值：点数<10认为稀疏

# 【V6】惯性系统参数 - 防止框图吸附和跳转
INERTIA_MIN_HISTORY = 3      # 最少3帧历史才启用惯性检查
INERTIA_ANGLE_THRESHOLD = 0.5  # cos(60°)，行人/普通目标的方向偏差阈值
INERTIA_ERROR_FACTOR = 2.0   # 行人/普通目标的预测误差容差系数
INERTIA_MIN_SPEED = 0.5      # 最小速度阈值，低于此值不检查方向

# 【V7新增】滑板车专用宽松惯性参数
INERTIA_ANGLE_THRESHOLD_SR = 0.3  # cos(70°)，滑板车允许更大转弯角度
INERTIA_ERROR_FACTOR_SR = 3.0     # 3倍预测误差容差，适应加速/减速场景

# 【V7新增】双阶段cy要求 - 平衡误判和连续性
SR_CY_MIN_CONVERT = 0.85     # Track→SR转换时的严格cy下限（防止行人误判）
SR_CY_MIN_TRACKING = 0.60    # SR关联跟踪时的宽松cy下限（保持连续跟踪）

# ================= V7版本信息输出 =================
print(f"[INFO] V7 Scooter Optimization Version - Data File: {CSV_FILE}")
print(f"[INFO] Dual-Track Strategy: Pedestrian Strict (Anti False-Positive) + Scooter Relaxed (Continuity)")
print(f"[INFO] MAX_MISS: Pedestrian {MAX_MISS} frames / Scooter {MAX_MISS_SR} frames")
print(f"[INFO] Conversion cy: {SR_CY_MIN_CONVERT}m / Tracking cy: {SR_CY_MIN_TRACKING}m")
print(f"[INFO] Inertia: Pedestrian 60° / Scooter 70°")

# 滑板车绘制
SCOOTER_BOX_WIDTH = 2.5
SCOOTER_COLOR_NORMAL = (1.0, 0.7, 0.0, 1.0)
SCOOTER_COLOR_DANGER = (1.0, 0.0, 0.0, 1.0)
SCOOTER_LABEL_COLOR = {
    "ESCOOTER-NORMAL": QtGui.QColor(255, 170, 0),
    "ESCOOTER-DANGER": QtGui.QColor(255, 64, 64),
}

try:
    from pyqtgraph.opengl import GLTextItem
    HAS_GLTEXT = True
except Exception:
    HAS_GLTEXT = False

# ================= 辅助函数 =================

def transform_xyz(x, y, z):
    return (z, y, -x) if ROTATE_Y_PLUS_90_FOR_X_ALIGNED_WALK else (x, y, z)


def load_frames(csv_file):
    """按 detIdx==0 分帧"""
    data, time_map, fid = {}, {}, -1
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            det_idx = int(row.get('detIdx', 0) or 0)
            if det_idx == 0:
                fid += 1
                data[fid] = []
                ts = row.get('timeStamp')
                if ts:
                    try:
                        time_map[fid] = datetime.fromisoformat(ts)
                    except Exception:
                        pass
            try:
                x, y, z = float(row['x']), float(row['y']), float(row['z'])
                if fid >= 0:
                    data[fid].append(transform_xyz(x, y, z))
            except Exception:
                continue
    
    frames = sorted(data.keys())
    if not frames:
        raise RuntimeError('No frames parsed from CSV')

    times = [time_map.get(fid) for fid in frames]
    ts_valid = [t for t in times if isinstance(t, datetime)]
    if len(ts_valid) >= 3:
        t0 = ts_valid[0]
        secs = np.array([(t - t0).total_seconds() for t in ts_valid], float)
        dts = np.diff(secs)
        dts = dts[dts > 0]
        dt_med = float(np.median(dts)) if dts.size else 0.05
    else:
        dt_med = 0.05

    rel_t = np.cumsum([0.0] + [dt_med]*(len(frames)-1)).astype(float)

    if ts_valid:
        base = ts_valid[0]
        abs_list = []
        for i, fid in enumerate(frames):
            t = time_map.get(fid)
            abs_list.append((t - base).total_seconds() if isinstance(t, datetime) else float(rel_t[i]))
        abs_t = np.array(abs_list, float)
    else:
        abs_t = rel_t.copy()

    return data, frames, rel_t, abs_t, dt_med


def grid_cluster(pts, cell=GRID_CELL_M, min_points=MIN_POINTS_IN_CLUSTER):
    """网格聚类"""
    if len(pts) == 0:
        return []
    P = np.asarray(pts)
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    off = 1000.0 * cell
    ix = np.floor((x + off) / cell).astype(np.int64)
    iz = np.floor((z + off) / cell).astype(np.int64)
    cell_map = defaultdict(list)
    for i, (cx, cz) in enumerate(zip(ix, iz)):
        cell_map[(cx, cz)].append(i)

    vis, clusters = set(), []
    from collections import deque as dq
    for key in list(cell_map.keys()):
        if key in vis:
            continue
        q = dq([key])
        vis.add(key)
        comp = []
        while q:
            c = q.popleft()
            comp.append(c)
            cx, cz = c
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == 0 and dz == 0:
                        continue
                    n = (cx + dx, cz + dz)
                    if n in cell_map and n not in vis:
                        vis.add(n)
                        q.append(n)
        idxs = []
        for c in comp:
            idxs.extend(cell_map[c])
        if len(idxs) >= min_points:
            cpts = P[idxs]
            xmin, xmax = float(cpts[:, 0].min()), float(cpts[:, 0].max())
            ymin, ymax = float(cpts[:, 1].min()), float(cpts[:, 1].max())
            zmin, zmax = float(cpts[:, 2].min()), float(cpts[:, 2].max())
            cxz = cpts[:, [0, 2]].mean(axis=0)
            clusters.append({
                "idxs": np.array(idxs, int),
                "pts": cpts,
                "centroid_xz": cxz,
                "bbox": (xmin, xmax, ymin, ymax, zmin, zmax)
            })
    return clusters


def make_bbox_lines(xmin, xmax, ymin, ymax, zmin, zmax):
    """生成边界框线段"""
    c000 = np.array([xmin, ymin, zmin])
    c100 = np.array([xmax, ymin, zmin])
    c010 = np.array([xmin, ymax, zmin])
    c110 = np.array([xmax, ymax, zmin])
    c001 = np.array([xmin, ymin, zmax])
    c101 = np.array([xmax, ymin, zmax])
    c011 = np.array([xmin, ymax, zmax])
    c111 = np.array([xmax, ymax, zmax])
    edges = [
        (c000, c100), (c100, c110), (c110, c010), (c010, c000),
        (c001, c101), (c101, c111), (c111, c011), (c011, c001),
        (c000, c001), (c100, c101), (c110, c111), (c010, c011)
    ]
    return np.vstack([np.vstack(e) for e in edges])


def is_scooter_rider(cluster, npts, strict=True, cy_hint=None, for_tracking=False):
    """
    【V7改进】判断是否为滑板车+人，双阶段cy策略
    
    for_tracking=False: 用于Track→SR转换（严格cy≥0.85）
    for_tracking=True: 用于SR关联（宽松cy≥0.60）
    """
    pt_min = SR_POINTS_MIN if strict else max(8, SR_POINTS_MIN - 7)
    pt_max = SR_POINTS_MAX if strict else SR_POINTS_MAX + 50
    
    if npts < pt_min or npts > pt_max:
        return False
    
    bbox = cluster["bbox"]
    xmin, xmax, ymin, ymax, zmin, zmax = bbox
    w, h, d = xmax - xmin, ymax - ymin, zmax - zmin
    
    tolerance = 1.0 if strict else 1.2
    
    if not (SR_WIDTH_MIN / tolerance <= w <= SR_WIDTH_MAX * tolerance):
        return False
    if not (SR_HEIGHT_MIN * 0.8 <= h <= SR_HEIGHT_MAX * tolerance):
        return False
    if not (SR_DEPTH_MIN / tolerance <= d <= SR_DEPTH_MAX * tolerance):
        return False
    
    # 质心高度检查
    pts = cluster.get("pts") if isinstance(cluster, dict) else None
    if pts is not None and len(pts) > 0:
        cy = float(np.asarray(pts)[:, 1].mean())
    elif cy_hint is not None:
        cy = float(cy_hint)
    else:
        cy = 0.5 * (ymin + ymax)
    
    # 【V7修复】cy异常值过滤：质心高度不应该超过3.0m（数据异常）
    if cy > 3.0:
        return False
    
    # 【V7核心改进】双阶段cy要求
    if for_tracking:
        # 关联检查：宽松cy要求（0.60），优先保持跟踪连续性
        cy_min = SR_CY_MIN_TRACKING  # 0.60m
        cy_max = SR_CENTROID_Y_MAX * 1.5  # 放宽上限
    else:
        # 转换检查：严格cy要求（0.85），防止行人误判
        cy_min = SR_CY_MIN_CONVERT  # 0.85m
        cy_max = SR_CENTROID_Y_MAX  # 5.0m
    
    if not (cy_min <= cy <= cy_max):
        return False
    
    # 强滑板车特征（降低要求，适应更多场景）
    if 0.75 <= cy <= 1.5 and npts >= 5:  # 放宽范围
        return True
    
    # 形状特征
    avg_horizontal = (w + d) / 2.0
    if npts >= 15:
        ratio_threshold = 0.6 if not strict else 0.8
        if avg_horizontal > 0 and h / avg_horizontal < ratio_threshold:
            return False
    
    return True


# ================= 【新增】改进的辅助函数 =================

def speed_stable(track, min_samples=5, stable_ratio=0.4):
    """
    【新增】检查轨迹速度是否稳定
    """
    if len(track.centroids) < min_samples:
        return False
    
    speeds = []
    Cs = np.array(list(track.centroids)[-min_samples:])
    Ts = np.array(list(track.times)[-min_samples:])
    
    for i in range(1, len(Cs)):
        dt = Ts[i] - Ts[i-1]
        if dt > 0:
            disp = np.hypot(Cs[i][0] - Cs[i-1][0], Cs[i][1] - Cs[i-1][1])
            speeds.append(disp / dt)
    
    if len(speeds) < 3:
        return False
    
    speeds = np.array(speeds)
    if speeds.mean() < 0.1:
        return False
    
    return (speeds.std() / speeds.mean()) < stable_ratio


def adaptive_association_gate(sr_track, base_gate, dt):
    """
    【新增】自适应关联门限
    """
    v = sr_track.speed_robust()
    speed_gate = v * dt * 3.0
    
    if len(sr_track.centroids) >= 3:
        speeds = []
        Cs = np.array(list(sr_track.centroids)[-5:])
        Ts = np.array(list(sr_track.times)[-5:])
        for i in range(1, min(len(Cs), 5)):
            dt_i = Ts[i] - Ts[i-1]
            if dt_i > 0:
                disp = np.hypot(Cs[i][0] - Cs[i-1][0], Cs[i][1] - Cs[i-1][1])
                speeds.append(disp / dt_i)
        
        if len(speeds) >= 2:
            acc = abs(speeds[-1] - speeds[-2]) / dt if dt > 0 else 0
            speed_gate += acc * dt * dt * 2.0
    
    final_gate = max(base_gate, speed_gate, 1.5)
    
    if v > 4.0:
        final_gate *= 1.3
    
    return final_gate


def predict_next_position(sr_track, dt):
    """
    【新增】预测下一帧位置
    """
    if len(sr_track.centroids) < 2:
        return sr_track.last()
    
    c_curr = np.array(sr_track.centroids[-1])
    c_prev = np.array(sr_track.centroids[-2])
    t_curr = sr_track.times[-1]
    t_prev = sr_track.times[-2]
    
    dt_hist = t_curr - t_prev
    if dt_hist <= 0:
        return tuple(c_curr.tolist())
    
    velocity = (c_curr - c_prev) / dt_hist
    predicted = c_curr + velocity * dt
    
    return tuple(predicted.tolist())


def validate_association(sr_track, cluster, current_time, max_speed_jump=8.0):  # 【V7】从6.0提高到8.0，适应加速场景
    """
    【V4终极修复】身份锁定后完全信任位置预测和自适应门限
    
    核心思想：
    1. 身份锁定后，目标已经稳定识别为电动滑板车+人
    2. V2的自适应门限和位置预测已经足够准确
    3. 稀疏点云（35%帧<10点）导致几何和速度特征不可靠
    4. 应该信任门限内的关联，而不是反复质疑
    """
    # 【关键修复】身份锁定后，完全信任门限内的关联
    if hasattr(sr_track, 'identity_locked') and sr_track.identity_locked:
        return True
    
    # 锁定前，进行极其宽松的验证（仅防止明显错误的转换）
    cx, cz = cluster["centroid_xz"]
    px, pz = sr_track.last()
    miss_count = sr_track.miss
    
    # 只在miss<5且有历史时做基本检查
    if len(sr_track.times) > 0 and miss_count < 5:
        dt = current_time - sr_track.times[-1]
        if dt > 0:
            instant_v = math.hypot(cx - px, cz - pz) / dt
            # 极宽松的阈值：只阻止物理不可能的速度（15m/s远超实际6m/s）
            if instant_v > 15.0:
                return False
    
    return True


def validate_inertia(track, new_cx, new_cz, dt, for_scooter=False):
    """
    【V7改进】惯性验证：防止框图跳转，双轨制参数
    
    for_scooter=False: 使用严格的行人参数（60度，2倍误差）
    for_scooter=True: 使用宽松的滑板车参数（70度，3倍误差）
    
    核心理念：
    - 轨迹应该沿着历史运动方向延续
    - 防止框图"吸附"到附近新出现的点云
    - 滑板车高速运动需要更宽松的约束
    
    返回: (is_valid, inertia_score)
    - is_valid: True=通过惯性检查, False=拒绝关联
    - inertia_score: 0-1，越大越符合惯性
    """
    # 历史太短，无法判断运动方向
    if len(track.centroids) < INERTIA_MIN_HISTORY:
        return True, 1.0
    
    # 获取最近的历史轨迹点
    recent_centroids = list(track.centroids)[-INERTIA_MIN_HISTORY:]
    recent_times = list(track.times)[-INERTIA_MIN_HISTORY:]
    
    # 计算历史运动向量（从最早到最近）
    hist_dx = recent_centroids[-1][0] - recent_centroids[0][0]
    hist_dz = recent_centroids[-1][1] - recent_centroids[0][1]
    hist_dt = recent_times[-1] - recent_times[0]
    
    if hist_dt <= 0:
        return True, 1.0
    
    # 历史速度
    hist_vx = hist_dx / hist_dt
    hist_vz = hist_dz / hist_dt
    hist_speed = math.sqrt(hist_vx**2 + hist_vz**2)
    
    # 如果历史速度很小（静止或慢速），放宽检查
    if hist_speed < INERTIA_MIN_SPEED:
        return True, 1.0
    
    # 新位置向量（从最近点到新位置）
    new_dx = new_cx - recent_centroids[-1][0]
    new_dz = new_cz - recent_centroids[-1][1]
    new_dist = math.sqrt(new_dx**2 + new_dz**2)
    
    # 如果新位置非常接近，不需要检查方向
    if new_dist < 0.1:
        return True, 1.0
    
    # 预测位置（基于匀速运动）
    pred_x = recent_centroids[-1][0] + hist_vx * dt
    pred_z = recent_centroids[-1][1] + hist_vz * dt
    
    # 预测误差
    pred_error = math.sqrt((new_cx - pred_x)**2 + (new_cz - pred_z)**2)
    
    # 方向一致性检查
    hist_norm = math.sqrt(hist_dx**2 + hist_dz**2)
    if hist_norm > 0.01:  # 避免除零
        # 历史方向单位向量
        hist_dir_x = hist_dx / hist_norm
        hist_dir_z = hist_dz / hist_norm
        
        # 新方向单位向量
        new_dir_x = new_dx / new_dist
        new_dir_z = new_dz / new_dist
        
        # 方向余弦（点积）cos(θ)
        cos_angle = hist_dir_x * new_dir_x + hist_dir_z * new_dir_z
        
        # 【V7改进】根据目标类型选择参数
        if for_scooter:
            angle_threshold = INERTIA_ANGLE_THRESHOLD_SR  # 0.3 (70度)
            error_factor = INERTIA_ERROR_FACTOR_SR  # 3.0
        else:
            angle_threshold = INERTIA_ANGLE_THRESHOLD  # 0.5 (60度)
            error_factor = INERTIA_ERROR_FACTOR  # 2.0
        
        # 角度差 > 90度（cos < 0），明显反向 -> 拒绝
        if cos_angle < -0.1:  # cos(95°) ≈ -0.087
            return False, 0.0
        
        # 角度差超过阈值，可疑 -> 降低分数
        if cos_angle < angle_threshold:
            inertia_score = max(0.0, cos_angle)
        else:
            inertia_score = 1.0
    else:
        inertia_score = 1.0
    
    # 【V7改进】预测误差检查：根据目标类型选择容差
    if for_scooter:
        error_factor = INERTIA_ERROR_FACTOR_SR  # 3.0
    else:
        error_factor = INERTIA_ERROR_FACTOR  # 2.0
    
    max_error = hist_speed * dt * error_factor
    
    if pred_error > max_error:
        # 偏离预测太远，降低分数
        error_ratio = max_error / (pred_error + 1e-6)
        inertia_score *= error_ratio
        
        # 偏离超过2倍，直接拒绝
        if pred_error > max_error * 2.0:
            return False, 0.0
    
    return True, inertia_score


def detect_scooter_occlusion(sr_track, clusters):
    """
    【V5优化】简化遮挡检测，减少误判
    只在点数极少时才判定为遮挡
    """
    # 【V5修复】只检查点数，移除"附近大目标"检测（过于激进）
    if sr_track.last_npts < 3:  # 从<5改为<3，更严格
        return True
    
    return False


def check_points_nearby(track_cx, track_cz, clusters, radius=0.6):
    """
    【V6新增】检查轨迹位置附近是否有点云
    
    用途：确保框图只显示在有实际点云的地方
    防止框图在空白区域遗留
    
    返回: True=有点云, False=无点云
    """
    for c in clusters:
        cx, cz = c["centroid_xz"]
        dist = math.sqrt((cx - track_cx)**2 + (cz - track_cz)**2)
        if dist <= radius:
            return True
    return False


def handle_sparse_frame(tracks, scooter_rider_tracks, now, total_points):
    """
    【新增】稀疏帧特殊处理：减少miss惩罚，延长latch
    当帧点数很少时(<10点)，不应该严厉惩罚miss
    """
    if total_points >= SR_SPARSE_FRAME_THRESHOLD:
        return  # 点云充足，不需要特殊处理
    
    # 稀疏帧：部分抵消miss
    for tr in tracks:
        if tr.miss > 0:
            tr.miss = max(0, tr.miss - 0.5)
    
    for sr in scooter_rider_tracks:
        if sr.miss > 0:
            sr.miss = max(0, sr.miss - 0.5)
        # 延长latch
        if sr.confirmed:
            sr.latch_until = max(sr.latch_until, now + 0.5)


# ================= Track 类 (简化版) =================

class Track:
    """简化的Track类,用于行人追踪"""
    _next = 1

    def __init__(self, cx, cz, t, yext, bbox=None, frame_idx=0, npts=0):
        self.id = Track._next
        Track._next += 1
        self.c_smooth = np.array([cx, cz], float)
        self.centroids = deque(maxlen=ROLL_WIN)
        self.times = deque(maxlen=ROLL_WIN)
        self.frames = deque(maxlen=ROLL_WIN)
        self.y_exts = deque(maxlen=ROLL_WIN)
        self.miss = 0
        self.score = 0
        self.confirmed = False
        self.latch_until = 0.0
        self.last_bbox = bbox
        self.last_npts = int(npts) if npts else 0
        
        self.yc_smooth = None
        self.y_base_smooth = None
        self.size = None
        self.lock_type = None
        
        self.add(cx, cz, t, yext, bbox=bbox, frame_idx=frame_idx, npts=npts)

    def add(self, cx, cz, t, yext, bbox=None, frame_idx=None, npts=None):
        self.c_smooth = (1 - EWMA_ALPHA) * self.c_smooth + EWMA_ALPHA * np.array([cx, cz], float)
        self.centroids.append((cx, cz))
        self.times.append(float(t))
        if frame_idx is not None:
            self.frames.append(int(frame_idx))
        self.y_exts.append(float(yext))
        if bbox is not None:
            self.last_bbox = bbox
            xmin, xmax, ymin, ymax, zmin, zmax = bbox
            yc = 0.5 * (ymin + ymax)
            self.yc_smooth = yc if self.yc_smooth is None else (1 - BOX_SMOOTH_ALPHA) * self.yc_smooth + BOX_SMOOTH_ALPHA * yc
            self.y_base_smooth = ymin if self.y_base_smooth is None else (1 - BOX_SMOOTH_ALPHA) * self.y_base_smooth + BOX_SMOOTH_ALPHA * ymin
            obs_size = np.array([xmax - xmin, ymax - ymin, zmax - zmin], float)
            self._update_size(obs_size)
        if npts is not None:
            self.last_npts = int(npts)
        self.miss = 0

    def last(self):
        return tuple(self.c_smooth.tolist())

    def last_frame(self):
        return self.frames[-1] if len(self.frames) > 0 else -1

    def duration(self):
        if len(self.times) < 2:
            return 0.0
        return self.times[-1] - self.times[0]

    def y_med(self):
        return float(np.median(self.y_exts)) if self.y_exts else 0.0

    def speed_robust(self):
        n = len(self.times)
        if n < 2:
            return 0.0
        k = min(n - 1, SPEED_WIN_PAIR)
        if k <= 0:
            return 0.0

        Cs = np.array(list(self.centroids)[-k - 1:], float)
        for i in range(1, Cs.shape[0]):
            Cs[i] = (1 - EWMA_ALPHA) * Cs[i - 1] + EWMA_ALPHA * Cs[i]
        Ts = np.array(list(self.times)[-k - 1:], float)

        dx, dz = np.diff(Cs[:, 0]), np.diff(Cs[:, 1])
        dt = np.diff(Ts)
        mask = dt > 0
        if not np.any(mask):
            return 0.0
        dx, dz, dt = dx[mask], dz[mask], dt[mask]

        disp = np.hypot(dx, dz)
        inst = disp / dt

        ok = (inst <= SPEED_SANITY_MAX) & (disp <= SPEED_SANITY_MAX * dt * DISP_FACTOR)
        good = inst[ok]
        if good.size == 0:
            return float(np.median(inst)) if inst.size else 0.0
        return float(np.median(good))

    def update_score_and_state(self, now):
        if self.lock_type == 'object':
            return False, self.speed_robust()

        dur = self.duration()
        v = self.speed_robust()
        ymed = self.y_med()
        ok = (dur >= MIN_DURATION_S) and (WALK_SPEED_LO <= v <= WALK_SPEED_HI) and (ymed >= Y_EXTENT_MIN)
        self.score = min(self.score + SCORE_HIT, 10) if ok else max(self.score - SCORE_MISS, 0)
        if (not self.confirmed) and self.score >= CONFIRM_SCORE:
            self.confirmed = True
            self.latch_until = now + LATCH_S
        if self.confirmed and self.score > 0:
            self.latch_until = max(self.latch_until, now + 0.2)
        show = self.confirmed and (now <= self.latch_until)
        return show, v

    def _update_size(self, obs_size: np.ndarray):
        mode = BOX_SIZE_MODE
        if mode == 'fixed' or obs_size is None:
            self.size = np.array(BOX_FIXED_WHD, float)
            return
        if mode == 'raw':
            self.size = np.clip(obs_size, BOX_SIZE_MIN_ARR, BOX_SIZE_MAX_ARR)
            return
        if self.size is None:
            seed = np.clip(obs_size, BOX_SIZE_MIN_ARR, BOX_SIZE_MAX_ARR)
            base = np.array(BOX_FIXED_WHD, float)
            self.size = 0.5 * base + 0.5 * seed
        else:
            prev = self.size
            target = np.clip(obs_size, BOX_SIZE_MIN_ARR, BOX_SIZE_MAX_ARR)
            up = prev * (1.0 + BOX_DELTA_CLAMP)
            dn = prev * (1.0 - BOX_DELTA_CLAMP)
            target = np.minimum(np.maximum(target, dn), up)
            self.size = (1.0 - BOX_SMOOTH_ALPHA) * prev + BOX_SMOOTH_ALPHA * target

    def display_bbox(self):
        if self.size is None:
            self.size = np.array(BOX_FIXED_WHD, float)
        w, h, d = self.size
        cx, cz = self.c_smooth
        pad = float(BOX_PAD)
        if BOX_ANCHOR == 'ground' and self.y_base_smooth is not None:
            ymin = self.y_base_smooth - pad
            ymax = ymin + h + 2 * pad
        else:
            yc = self.yc_smooth if self.yc_smooth is not None else 0.5 * h
            ymin = (yc - 0.5 * h) - pad
            ymax = (yc + 0.5 * h) + pad
        xmin = (cx - 0.5 * w) - pad
        xmax = (cx + 0.5 * w) + pad
        zmin = (cz - 0.5 * d) - pad
        zmax = (cz + 0.5 * d) + pad
        return xmin, xmax, ymin, ymax, zmin, zmax


# ================= 【改进】ScooterRiderTrack 类 =================

class ScooterRiderTrack:
    """
    【改进】滑板车+人追踪类
    新增身份锁定机制
    """
    _next_sr = 1

    def __init__(self, cx, cz, t, bbox, frame_idx, npts):
        self.id = ScooterRiderTrack._next_sr
        ScooterRiderTrack._next_sr += 1
        self.c_smooth = np.array([cx, cz], float)
        self.centroids = deque(maxlen=ROLL_WIN)
        self.times = deque(maxlen=ROLL_WIN)
        self.frames = deque(maxlen=ROLL_WIN)
        self.miss = 0
        self.score = 0
        self.confirmed = False
        self.latch_until = 0.0
        self.last_bbox = bbox
        self.last_npts = int(npts)
        
        xmin, xmax, ymin, ymax, zmin, zmax = bbox
        self.cy_smooth = 0.5 * (ymin + ymax)
        self.size = np.array([xmax - xmin, ymax - ymin, zmax - zmin], float)
        
        # 【新增】身份锁定机制
        self.identity_locked = False
        self.lock_time = 0
        
        self.add(cx, cz, t, bbox, frame_idx, npts)

    def add(self, cx, cz, t, bbox, frame_idx, npts):
        self.c_smooth = (1 - EWMA_ALPHA) * self.c_smooth + EWMA_ALPHA * np.array([cx, cz], float)
        self.centroids.append((cx, cz))
        self.times.append(float(t))
        self.frames.append(int(frame_idx))
        self.last_bbox = bbox
        self.last_npts = int(npts)
        
        xmin, xmax, ymin, ymax, zmin, zmax = bbox
        cy = 0.5 * (ymin + ymax)
        self.cy_smooth = (1 - BOX_SMOOTH_ALPHA) * self.cy_smooth + BOX_SMOOTH_ALPHA * cy
        obs_size = np.array([xmax - xmin, ymax - ymin, zmax - zmin], float)
        self.size = (1 - BOX_SMOOTH_ALPHA) * self.size + BOX_SMOOTH_ALPHA * obs_size
        
        self.miss = 0

    def last(self):
        return tuple(self.c_smooth.tolist())

    def last_frame(self):
        return self.frames[-1] if len(self.frames) > 0 else -1

    def duration(self):
        if len(self.times) < 2:
            return 0.0
        return self.times[-1] - self.times[0]

    def speed_robust(self):
        n = len(self.times)
        if n < 2:
            return 0.0
        k = min(n - 1, SPEED_WIN_PAIR)
        if k <= 0:
            return 0.0

        Cs = np.array(list(self.centroids)[-k - 1:], float)
        for i in range(1, Cs.shape[0]):
            Cs[i] = (1 - EWMA_ALPHA) * Cs[i - 1] + EWMA_ALPHA * Cs[i]
        Ts = np.array(list(self.times)[-k - 1:], float)

        dx, dz = np.diff(Cs[:, 0]), np.diff(Cs[:, 1])
        dt = np.diff(Ts)
        mask = dt > 0
        if not np.any(mask):
            return 0.0
        dx, dz, dt = dx[mask], dz[mask], dt[mask]

        disp = np.hypot(dx, dz)
        inst = disp / dt

        ok = (inst <= SPEED_SANITY_MAX) & (disp <= SPEED_SANITY_MAX * dt * DISP_FACTOR)
        good = inst[ok]
        if good.size == 0:
            return float(np.median(inst)) if inst.size else 0.0
        return float(np.median(good))

    def update_state(self, now):
        dur = self.duration()
        v = self.speed_robust()
        
        cond = (dur >= SR_MIN_DURATION_S) and (SR_SPEED_MIN <= v <= SR_SPEED_MAX)
        
        self.score = min(self.score + SR_SCORE_HIT, 10) if cond else max(self.score - SR_SCORE_MISS, 0)
        
        if (not self.confirmed) and self.score >= SR_CONFIRM_SCORE:
            self.confirmed = True
            self.latch_until = now + SR_LATCH_S
        
        if self.confirmed and self.score > 0:
            self.latch_until = max(self.latch_until, now + 0.2)
        
        show = self.confirmed and (now <= self.latch_until)
        return show, v

    def display_bbox(self):
        w, h, d = self.size
        cx, cz = self.c_smooth
        cy = self.cy_smooth
        pad = 0.1
        
        xmin = (cx - 0.5 * w) - pad
        xmax = (cx + 0.5 * w) + pad
        ymin = (cy - 0.5 * h) - pad
        ymax = (cy + 0.5 * h) + pad
        zmin = (cz - 0.5 * d) - pad
        zmax = (cz + 0.5 * d) + pad
        
        return xmin, xmax, ymin, ymax, zmin, zmax
    
    def lock_identity(self, now):
        """【新增】锁定身份"""
        self.identity_locked = True
        self.lock_time = now


# ================= 主程序 =================

def main():
    print("[INFO] ========================================")
    print("[INFO] AAA_TEST Improved Version Starting")
    print("[INFO] ========================================")
    print(f"[INFO] Improved Parameters:")
    print(f"[INFO]   SR_HEIGHT_MIN: {SR_HEIGHT_MIN}m (was 0.30m)")
    print(f"[INFO]   SR_CENTROID_Y_MIN: {SR_CENTROID_Y_MIN}m (was 0.20m)")
    print(f"[INFO]   Speed Threshold: Two-level (was Three-level)")
    print(f"[INFO]   Association Gate: Adaptive (was Fixed)")
    print("[INFO] ========================================")
    
    data, frames, rel_t, abs_t, dt_med = load_frames(CSV_FILE)
    total_time = rel_t[-1] if len(rel_t) else 0.0

    assoc_gate = max(ASSOC_GATE_BASE_M, SPEED_SANITY_MAX * dt_med * 2.0)

    app = QtWidgets.QApplication([])
    view = gl.GLViewWidget()
    view.opts['distance'] = 20
    view.setCameraPosition(azimuth=45, elevation=20, distance=20)
    view.setWindowTitle(f'Radar 3D [IMPROVED] - {os.path.basename(CSV_FILE)}')
    view.show()
    
    axis = gl.GLAxisItem()
    axis.setSize(x=10, y=10, z=10)
    view.addItem(axis)
    
    grid = gl.GLGridItem()
    grid.setSize(10, 10)
    grid.setSpacing(1, 1)
    view.addItem(grid)
    
    scatter = gl.GLScatterPlotItem(size=POINT_SIZE, color=PT_COLOR)
    view.addItem(scatter)

    box_items, text_items = [], []
    tracks = []
    scooter_rider_tracks = []

    timer = QtCore.QTimer()
    timer.setInterval(max(int(dt_med * 1000), 20))
    elapsed = QtCore.QElapsedTimer()
    elapsed.start()
    idx = 0

    def clear_tracks():
        nonlocal tracks, scooter_rider_tracks
        tracks.clear()
        scooter_rider_tracks.clear()
        Track._next = 1
        ScooterRiderTrack._next_sr = 1

    def update():
        nonlocal idx, box_items, text_items, tracks, scooter_rider_tracks
        sec = elapsed.elapsed() / 1000.0
        
        if total_time > 0 and sec > total_time:
            elapsed.restart()
            idx = 0
            sec = 0.0
            clear_tracks()

        while idx < len(frames) - 1 and sec >= rel_t[idx + 1]:
            idx += 1

        pts = np.array(data[frames[idx]], float) if data[frames[idx]] else np.zeros((0, 3))
        scatter.setData(pos=pts)

        for it in box_items:
            view.removeItem(it)
        box_items = []
        for it in text_items:
            view.removeItem(it)
        text_items = []

        clusters = grid_cluster(pts)
        
        # 【新增】稀疏帧处理
        total_points = len(pts)
        handle_sparse_frame(tracks, scooter_rider_tracks, abs_t[idx], total_points)

        for tr in tracks:
            tr.miss += 1
        for sr in scooter_rider_tracks:
            sr.miss += 1

        used = [False] * len(clusters)

        # 【改进】ScooterRider 关联 - 使用新的关联逻辑
        for sr in scooter_rider_tracks:
            best = None
            bestd = None
            best_ci = None
            
            # 【改进1】使用预测位置
            px, pz = predict_next_position(sr, dt_med)
            
            # 【V7改进】增大滑板车关联门限倍数（1.8→2.5）
            sr_gate = adaptive_association_gate(sr, assoc_gate * 2.5, dt_med)
            
            for ci, c in enumerate(clusters):
                if used[ci]:
                    continue
                
                cx, cz = c["centroid_xz"]
                d = math.hypot(cx - px, cz - pz)
                
                if d <= sr_gate and (bestd is None or d < bestd):
                    bestd = d
                    best = c
                    best_ci = ci
            
            if best is not None:
                cx, cz = best["centroid_xz"]
                
                # 【V7改进】使用滑板车专用惯性参数
                inertia_valid, inertia_score = validate_inertia(sr, cx, cz, dt_med, for_scooter=True)
                
                if not inertia_valid:
                    print(f"  [INERTIA-REJECT] SR#{sr.id} inertia check failed, score={inertia_score:.2f} d={bestd:.2f}m")
                    best = None
                    best_ci = None
                elif validate_association(sr, best, abs_t[idx], SR_MAX_SPEED_JUMP):
                    # 通过惯性和关联验证
                    used[best_ci] = True
                    npts = len(best["idxs"])
                    sr.add(cx, cz, abs_t[idx], best["bbox"], idx, npts)
                    
                    if inertia_score < 0.8:
                        print(f"  [INERTIA-WEAK] SR#{sr.id} low inertia score={inertia_score:.2f}")
                    
                    # 确认后锁定身份
                    if sr.confirmed and not sr.identity_locked:
                        sr.lock_identity(abs_t[idx])
                        print(f"[LOCK] SR#{sr.id} identity locked")
                else:
                    print(f"  [REJECT-ASSOC] SR#{sr.id} association validation failed, d={bestd:.2f}m gate={sr_gate:.2f}m")
                    best = None
            
            if best is None:
                # 【V6修改】移除遮挡检测的miss减免（更快清理）
                pass

        # 普通Track关联
        for ci, c in enumerate(clusters):
            if used[ci]:
                continue
            cx, cz = c["centroid_xz"]
            xmin, xmax, ymin, ymax, zmin, zmax = c["bbox"]
            yext = ymax - ymin
            npts = len(c["idxs"])
            
            best = None
            bestd = None
            for tr in tracks:
                if tr.last_frame() >= idx:
                    continue
                px, pz = tr.last()
                d = math.hypot(cx - px, cz - pz)
                if d <= assoc_gate and (bestd is None or d < bestd):
                    bestd = d
                    best = tr
            
            if best is not None:
                used[ci] = True
                best.add(cx, cz, abs_t[idx], yext, bbox=c["bbox"], frame_idx=idx, npts=npts)

        # 【V5改进】Track → ScooterRider 转换 (三级策略)
        tracks_to_convert = []
        for i, tr in enumerate(tracks):
            if tr.lock_type == 'object':
                continue
            
            if tr.last_bbox is None or len(tr.centroids) < 2:
                continue
                
            temp_cluster = {"bbox": tr.last_bbox}
            v = tr.speed_robust()
            cy = tr.yc_smooth if tr.yc_smooth is not None else 0
            
            # 【V7改进】第零级: 极高速快速通道 (v >= 4.0 m/s，cy >= 0.75)
            # 降低cy要求以覆盖远距离/角度偏移的滑板车
            if v >= 4.0 and cy >= 0.75:  # 从4.5/0.90降低到4.0/0.75
                if tr.last_npts >= 5:
                    tracks_to_convert.append((i, tr, 'very_high_speed'))
                    print(f"  [CONVERT-L0] Track#{tr.id}→SR v={v:.2f}m/s cy={cy:.2f}m (Fast Lane)")
                    continue
            
            # 【V7改进】第一级: 明确高速 (v >= 2.8 m/s，cy >= 0.85)
            # 平衡速度和cy：避免慢跑行人（v<2.8, cy<0.6），又能识别滑板车
            if v >= 2.8:
                if is_scooter_rider(temp_cluster, tr.last_npts, strict=False, cy_hint=cy, for_tracking=False):
                    # cy检查在is_scooter_rider内确保>=0.85（SR_CY_MIN_CONVERT）
                    tracks_to_convert.append((i, tr, 'high_speed'))
                    print(f"  [CONVERT-L1] Track#{tr.id}→SR v={v:.2f}m/s cy={cy:.2f}m npts={tr.last_npts}")
                    continue
            
            # 【V7改进】第二级: 中速+强特征 (v >= 2.0 m/s，cy >= 0.90，dur >= 1.0s)
            # 放宽要求以识别慢速滑板车，但保持足够严格避免误判
            elif v >= 2.0:
                if (is_scooter_rider(temp_cluster, tr.last_npts, strict=True, cy_hint=cy, for_tracking=False) 
                    and cy >= 0.90  # 从1.2降低到0.90
                    and cy <= 2.5  # 放宽上限
                    and tr.duration() >= 1.0):  # 从2.0降低到1.0s
                    
                    tracks_to_convert.append((i, tr, 'medium_speed'))
                    print(f"  [CONVERT-L2] Track#{tr.id}→SR v={v:.2f}m/s cy={cy:.2f}m dur={tr.duration():.2f}s npts={tr.last_npts}")
        
        # 执行转换
        for item in reversed(tracks_to_convert):
            i, old_tr, speed_level = item
            cx, cz = old_tr.last()
            
            sr = ScooterRiderTrack(cx, cz, abs_t[idx], old_tr.last_bbox, idx, old_tr.last_npts)
            
            n_keep = min(10, len(old_tr.centroids))
            if n_keep > 0:
                for j in range(-n_keep, 0):
                    sr.centroids.append(old_tr.centroids[j])
                    sr.times.append(old_tr.times[j])
                    sr.frames.append(old_tr.frames[j])
            
            scooter_rider_tracks.append(sr)
            del tracks[i]
            
            v_actual = old_tr.speed_robust()
            cy_actual = old_tr.yc_smooth if old_tr.yc_smooth is not None else 0
            print(f"[CONVERT] Track#{old_tr.id} → ScooterRider#{sr.id} (v={v_actual:.2f}m/s, level={speed_level}, cy={cy_actual:.2f}m)")

        # 新建轨迹
        for ci, c in enumerate(clusters):
            if used[ci]:
                continue
            cx, cz = c["centroid_xz"]
            xmin, xmax, ymin, ymax, zmin, zmax = c["bbox"]
            npts = len(c["idxs"])
            
            tr = Track(cx, cz, abs_t[idx], ymax - ymin, bbox=c["bbox"], frame_idx=idx, npts=npts)
            tracks.append(tr)

        # 清理超时轨迹
        # 【V5修复】不同类型轨迹使用不同的miss阈值
        tracks = [tr for tr in tracks if tr.miss <= MAX_MISS]
        scooter_rider_tracks = [sr for sr in scooter_rider_tracks if sr.miss <= MAX_MISS_SR]

        # 显示
        ped_count = 0
        sr_count = 0
        
        # 显示 ScooterRider
        for sr in scooter_rider_tracks:
            show, v = sr.update_state(abs_t[idx])
            if show:
                # 【V7修改】移除滑板车的点云存在强制检查
                # 高速滑板车点云间断正常，强制检查会导致显示闪烁
                # 依靠MAX_MISS_SR=12控制清理时间
                
                sr_count += 1
                bbox = sr.display_bbox()
                xmin, xmax, ymin, ymax, zmin, zmax = bbox
                lines = make_bbox_lines(xmin, xmax, ymin, ymax, zmin, zmax)
                
                color = SCOOTER_COLOR_DANGER if v >= SR_SPEED_DANGER else SCOOTER_COLOR_NORMAL
                box = gl.GLLinePlotItem(pos=lines, color=color, width=SCOOTER_BOX_WIDTH, antialias=True)
                view.addItem(box)
                box_items.append(box)
                
                if HAS_GLTEXT and LABEL_SPEED:
                    status = "DANGER" if v >= SR_SPEED_DANGER else "NORMAL"
                    miss_info = f" [M:{sr.miss}]" if sr.miss > 0 else ""
                    lbl = f"ESCOOTER-{status}\nID:{sr.id}\nv={v:.1f}m/s{miss_info}"
                    txt = GLTextItem(pos=(xmax, ymax, zmax), text=lbl, 
                                    color=SCOOTER_LABEL_COLOR[f"ESCOOTER-{status}"])
                    view.addItem(txt)
                    text_items.append(txt)

        # 显示 Pedestrian
        for tr in tracks:
            show, v = tr.update_score_and_state(abs_t[idx])
            if show:
                # 【V6新增】行人也检查点云存在
                cx, cz = tr.last()
                if not check_points_nearby(cx, cz, clusters, radius=0.6):
                    continue
                
                ped_count += 1
                bbox = tr.display_bbox()
                xmin, xmax, ymin, ymax, zmin, zmax = bbox
                lines = make_bbox_lines(xmin, xmax, ymin, ymax, zmin, zmax)
                
                box = gl.GLLinePlotItem(pos=lines, color=BOX_COLOR, width=BOX_WIDTH, antialias=True)
                view.addItem(box)
                box_items.append(box)
                
                if HAS_GLTEXT and LABEL_SPEED:
                    miss_info = f" [M:{tr.miss}]" if tr.miss > 0 else ""
                    lbl = f"Pedestrian\nID:{tr.id}\nv={v:.1f}m/s{miss_info}"
                    txt = GLTextItem(pos=(xmax, ymax, zmax), text=lbl, color=QtGui.QColor(0, 255, 0))
                    view.addItem(txt)
                    text_items.append(txt)

        # 【改进】显示更多调试信息
        sparse_marker = " [SPARSE]" if total_points < SR_SPARSE_FRAME_THRESHOLD else ""
        view.setWindowTitle(f'Radar 3D [V2] - {sec:.2f}s | Pts:{total_points} | Ped:{ped_count} SR:{sr_count}{sparse_marker} | {os.path.basename(CSV_FILE)}')

    timer.timeout.connect(update)
    timer.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

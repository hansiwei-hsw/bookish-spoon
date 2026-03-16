import os
import json
from typing import Any, Dict


class ConfigHandler:
    """配置模块：管理系统配置（角度/弧度、小数位数、兼容模式）"""

    DEFAULT_CONFIG = {
        "use_degree": True,
        "decimal_places": 4,
        "compatibility_mode": False,
        "scientific_threshold": 1e6
    }

    def __init__(self, config_file: str = "calculator_config.json"):
        """初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self._config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self._load_config()

    def _load_config(self):
        """从文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self._config.update(loaded)
            except (json.JSONDecodeError, IOError, PermissionError):
                pass

    def _save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except (IOError, PermissionError):
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置项名称
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any, save: bool = True):
        """设置配置值
        
        Args:
            key: 配置项名称
            value: 配置值
            save: 是否立即保存到文件
        """
        if key in self._config:
            self._config[key] = value
            if save:
                self._save_config()

    @property
    def use_degree(self) -> bool:
        """是否使用角度模式"""
        return self._config.get("use_degree", True)

    @use_degree.setter
    def use_degree(self, value: bool):
        """设置角度/弧度模式"""
        self._config["use_degree"] = bool(value)
        self._save_config()

    @property
    def decimal_places(self) -> int:
        """默认保留小数位数"""
        return self._config.get("decimal_places", 4)

    @decimal_places.setter
    def decimal_places(self, value: int):
        """设置默认保留小数位数"""
        if 0 <= value <= 10:
            self._config["decimal_places"] = value
            self._save_config()

    @property
    def compatibility_mode(self) -> bool:
        """是否启用兼容模式"""
        return self._config.get("compatibility_mode", False)

    @compatibility_mode.setter
    def compatibility_mode(self, value: bool):
        """设置兼容模式"""
        self._config["compatibility_mode"] = bool(value)
        self._save_config()

    @property
    def scientific_threshold(self) -> float:
        """科学计数法阈值"""
        return self._config.get("scientific_threshold", 1e6)

    @scientific_threshold.setter
    def scientific_threshold(self, value: float):
        """设置科学计数法阈值"""
        if value > 0:
            self._config["scientific_threshold"] = value
            self._save_config()

    def toggle_angle_mode(self) -> bool:
        """切换角度/弧度模式
        
        Returns:
            切换后的模式状态（True表示角度）
        """
        self.use_degree = not self.use_degree
        return self.use_degree

    def toggle_compatibility_mode(self) -> bool:
        """切换兼容模式
        
        Returns:
            切换后的模式状态
        """
        self.compatibility_mode = not self.compatibility_mode
        return self.compatibility_mode

    def reset_defaults(self):
        """重置所有配置为默认值"""
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()

    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置项
        
        Returns:
            配置字典副本
        """
        return self._config.copy()

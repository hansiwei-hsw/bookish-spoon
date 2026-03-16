"""
配置管理模块
负责管理系统配置，包括角度/弧度模式、小数位数、兼容模式等
"""
import json
import os
from typing import Dict, Any


class ConfigHandler:
    """
    配置管理器类
    负责加载、保存、管理计算器配置
    """
    
    DEFAULT_CONFIG = {
        'angle_mode': 'degree',
        'decimal_places': 4,
        'compatibility_mode': False,
        'scientific_notation_threshold': 1e10,
        'history_max_records': 100,
        'cache_enabled': True,
        'cache_max_size': 100
    }
    
    CONFIG_FILE = 'calculator_config.json'
    
    def __init__(self):
        """初始化配置管理器"""
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """从文件加载配置，如果文件不存在则使用默认配置"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self._config = {**self.DEFAULT_CONFIG, **loaded_config}
            except (json.JSONDecodeError, IOError, PermissionError):
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """保存配置到文件"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
            return True
        except (IOError, PermissionError):
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置项并持久化保存"""
        if key in self.DEFAULT_CONFIG:
            self._config[key] = value
            return self.save_config()
        return False
    
    def get_angle_mode(self) -> str:
        """获取角度模式（degree/radian）"""
        return self._config.get('angle_mode', 'degree')
    
    def set_angle_mode(self, mode: str) -> bool:
        """设置角度模式"""
        if mode in ('degree', 'radian'):
            return self.set('angle_mode', mode)
        return False
    
    def get_decimal_places(self) -> int:
        """获取小数位数"""
        return self._config.get('decimal_places', 4)
    
    def set_decimal_places(self, places: int) -> bool:
        """设置小数位数"""
        if 0 <= places <= 15:
            return self.set('decimal_places', places)
        return False
    
    def is_compatibility_mode(self) -> bool:
        """检查是否启用兼容模式"""
        return self._config.get('compatibility_mode', False)
    
    def set_compatibility_mode(self, enabled: bool) -> bool:
        """设置兼容模式"""
        return self.set('compatibility_mode', enabled)
    
    def is_cache_enabled(self) -> bool:
        """检查是否启用缓存"""
        return self._config.get('cache_enabled', True)
    
    def get_cache_max_size(self) -> int:
        """获取缓存最大容量"""
        return self._config.get('cache_max_size', 100)
    
    def get_scientific_threshold(self) -> float:
        """获取科学计数法阈值"""
        return self._config.get('scientific_notation_threshold', 1e10)
    
    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        self._config = self.DEFAULT_CONFIG.copy()
        return self.save_config()
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()


_config_instance = None


def get_config() -> ConfigHandler:
    """获取配置管理器单例"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigHandler()
    return _config_instance

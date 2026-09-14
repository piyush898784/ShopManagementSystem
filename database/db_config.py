"""
Database Configuration and Connection Management for Shop Management System.
Supports MySQL with dynamic credential management and quick timeout protection.
"""

import json
import os
from typing import Optional, Dict, Any

try:
    import pymysql
    import pymysql.cursors
    MySQLError = pymysql.MySQLError
    CONNECTOR_TYPE = "pymysql"
except ImportError:
    try:
        import mysql.connector
        from mysql.connector import Error as MySQLError
        CONNECTOR_TYPE = "mysql.connector"
    except ImportError:
        CONNECTOR_TYPE = None
        MySQLError = Exception


class DatabaseConfig:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
    DEFAULT_CONFIG = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "",
        "database": "shop_management_db"
    }

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Loads MySQL connection configuration from file or returns default."""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    config = cls.DEFAULT_CONFIG.copy()
                    config.update(data)
                    return config
            except Exception:
                pass
        return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> bool:
        """Saves MySQL connection configuration to file."""
        try:
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            return True
        except Exception:
            return False

    @classmethod
    def get_connection(cls, include_database: bool = True):
        """
        Creates and returns an active MySQL connection with fast timeout to prevent UI lag.
        """
        config = cls.load_config()
        host = config.get("host", "localhost")
        port = int(config.get("port", 3306))
        user = config.get("user", "root")
        password = config.get("password", "")
        database = config.get("database", "shop_management_db") if include_database else None

        if CONNECTOR_TYPE == "pymysql":
            kwargs = {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "autocommit": False,
                "connect_timeout": 2,
                "cursorclass": pymysql.cursors.DictCursor
            }
            if database:
                kwargs["database"] = database
            return pymysql.connect(**kwargs)
        elif CONNECTOR_TYPE == "mysql.connector":
            kwargs = {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "connection_timeout": 2,
                "autocommit": False
            }
            if database:
                kwargs["database"] = database
            return mysql.connector.connect(**kwargs)
        else:
            raise RuntimeError("No MySQL driver found! Please install 'mysql-connector-python' or 'pymysql'.")

    @classmethod
    def test_connection(cls, config: Optional[Dict[str, Any]] = None) -> tuple[bool, str]:
        """Tests connection with the given or saved credentials."""
        cfg = config if config is not None else cls.load_config()
        host = cfg.get("host", "localhost")
        port = int(cfg.get("port", 3306))
        user = cfg.get("user", "root")
        password = cfg.get("password", "")

        try:
            if CONNECTOR_TYPE == "pymysql":
                conn = pymysql.connect(
                    host=host, port=port, user=user, password=password, connect_timeout=2
                )
                conn.close()
            elif CONNECTOR_TYPE == "mysql.connector":
                conn = mysql.connector.connect(
                    host=host, port=port, user=user, password=password, connection_timeout=2
                )
                conn.close()
            else:
                return False, "MySQL driver not installed."
            return True, "Connection successful!"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

#!/usr/bin/env python3
"""
config.py - Module de gestion de la configuration pour le bot HFT
Centralise tous les paramètres du bot, y compris les clés API, paires de trading, et paramètres de stratégie
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional

class Config:
    """
    Classe de gestion de la configuration du bot HFT
    """
    # Valeurs par défaut
    DEFAULT_CONFIG = {
        # Paramètres généraux
        "LOOP_INTERVAL": 0.1,  # Fréquence de la boucle principale en secondes (0.1 = 10 fois par seconde)
        "USE_TESTNET": True,   # Utiliser le testnet Binance par défaut pour la sécurité
        "DB_PATH": "data/trading_data.db",
        "LOG_LEVEL": "INFO",
        "SYMBOL": "BTCUSDT",  # Paire de trading par défaut
        
        # Clés API (à remplacer par les vraies valeurs)
        "API_KEY": "",
        "API_SECRET": "",
        
        # Paramètres de notification
        "EMAIL_CONFIG": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "receiver_email": "",
            "password": ""
        },
        "TELEGRAM_CONFIG": {
            "enabled": False,
            "token": "",
            "chat_id": ""
        },
        
        # Paramètres de gestion des risques
        "MAX_POSITION_SIZE": 0.01,      # Taille max de position en BTC (ou autre crypto)
        "MAX_RISK_PER_TRADE": 0.02,     # Risque max par trade (2% du capital)
        "MAX_DAILY_LOSS": 0.05,         # Perte max quotidienne (5% du capital)
        "MAX_OPEN_ORDERS": 10,          # Nombre maximum d'ordres ouverts simultanément
        "MAX_TRADES_PER_DAY": 500,      # Nombre maximum de trades par jour
        
        # Paramètres de stratégie Market Making
        "STRATEGY": "market_making",    # Stratégie par défaut
        "MM_SPREAD": 0.002,             # Spread pour market making (0.2%)
        "MM_ORDER_SIZE": 0.001,         # Taille des ordres pour market making (en BTC)
        "MM_ORDER_COUNT": 3,            # Nombre de niveaux d'ordres
        "MM_REFRESH_RATE": 1,           # Taux de rafraîchissement des ordres (secondes)
        
        # Paramètres de stratégie Arbitrage
        "ARBITRAGE_SYMBOLS": ["BTCUSDT", "ETHUSDT", "ETHBTC"],
        "MIN_PROFIT_THRESHOLD": 0.003,  # Seuil de profit minimum pour l'arbitrage (0.3%)
        
        # Paramètres de stratégie Momentum
        "MOMENTUM_TIMEFRAME": "1m",     # Timeframe pour la stratégie momentum
        "LOOKBACK_PERIOD": 20,          # Période de lookback pour les indicateurs
        "RSI_PERIOD": 14,               # Période RSI
        "RSI_OVERBOUGHT": 70,           # Seuil de surachat RSI
        "RSI_OVERSOLD": 30,             # Seuil de survente RSI
        "EMA_SHORT": 9,                 # EMA court terme
        "EMA_LONG": 21,                 # EMA long terme
        
        # Paires de trading disponibles
        "AVAILABLE_PAIRS": [
            "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT",
            "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT"
        ],
        
        # Timeframes disponibles
        "AVAILABLE_TIMEFRAMES": ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"]
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialise la configuration depuis un fichier JSON ou utilise les valeurs par défaut
        
        :param config_path: Chemin vers le fichier de configuration JSON
        """
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.config_data = {}
        
        # Chargement de la configuration
        self._load_config()
        
        # Chargement des variables d'environnement (prioritaires sur le fichier config)
        self._load_env_variables()
        
        # Validation de la configuration
        self._validate_config()
        
        # Définition des attributs de classe à partir de la configuration
        for key, value in self.config_data.items():
            setattr(self, key, value)
    
    def _load_config(self) -> None:
        """
        Charge la configuration depuis le fichier JSON ou utilise les valeurs par défaut
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as config_file:
                    user_config = json.load(config_file)
                    
                # Fusion avec les valeurs par défaut
                self.config_data = {**self.DEFAULT_CONFIG, **user_config}
                self.logger.info(f"Configuration chargée depuis {self.config_path}")
            else:
                self.config_data = self.DEFAULT_CONFIG.copy()
                self.logger.warning(f"Fichier de configuration {self.config_path} non trouvé. Utilisation des valeurs par défaut.")
                
                # Création du fichier de configuration par défaut
                self._save_default_config()
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la configuration: {str(e)}")
            self.config_data = self.DEFAULT_CONFIG.copy()
    
    def _save_default_config(self) -> None:
        """
        Sauvegarde la configuration par défaut dans un fichier JSON
        """
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as config_file:
                json.dump(self.DEFAULT_CONFIG, config_file, indent=4)
            self.logger.info(f"Fichier de configuration par défaut créé à {self.config_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du fichier de configuration par défaut: {str(e)}")
    
    def _load_env_variables(self) -> None:
        """
        Charge les variables d'environnement pour les clés sensibles
        Les variables d'environnement ont la priorité sur le fichier de configuration
        """
        # Clés API
        if os.environ.get('BINANCE_API_KEY'):
            self.config_data['API_KEY'] = os.environ.get('BINANCE_API_KEY')
            self.logger.info("Clé API chargée depuis les variables d'environnement")
        
        if os.environ.get('BINANCE_API_SECRET'):
            self.config_data['API_SECRET'] = os.environ.get('BINANCE_API_SECRET')
            self.logger.info("Clé API secrète chargée depuis les variables d'environnement")
        
        # Autres variables d'environnement potentielles
        env_mapping = {
            'BOT_USE_TESTNET': ('USE_TESTNET', lambda x: x.lower() == 'true'),
            'BOT_SYMBOL': ('SYMBOL', str),
            'BOT_MAX_POSITION_SIZE': ('MAX_POSITION_SIZE', float),
            'BOT_STRATEGY': ('STRATEGY', str)
        }
        
        for env_name, (config_name, converter) in env_mapping.items():
            if os.environ.get(env_name):
                self.config_data[config_name] = converter(os.environ.get(env_name))
                self.logger.info(f"{config_name} chargé depuis les variables d'environnement")
    
    def _validate_config(self) -> None:
        """
        Valide la configuration et affiche des avertissements pour les paramètres manquants ou invalides
        """
        # Vérification des clés API
        if not self.config_data.get('API_KEY') or not self.config_data.get('API_SECRET'):
            self.logger.warning("Clés API Binance manquantes. Configurez API_KEY et API_SECRET.")
        
        # Vérification de la paire de trading
        if self.config_data.get('SYMBOL') not in self.config_data.get('AVAILABLE_PAIRS'):
            self.logger.warning(f"Paire de trading {self.config_data.get('SYMBOL')} non disponible. "
                              f"Paires disponibles: {', '.join(self.config_data.get('AVAILABLE_PAIRS'))}")
        
        # Vérification de la stratégie
        valid_strategies = ['market_making', 'arbitrage', 'momentum']
        if self.config_data.get('STRATEGY') not in valid_strategies:
            self.logger.warning(f"Stratégie {self.config_data.get('STRATEGY')} non valide. "
                              f"Stratégies disponibles: {', '.join(valid_strategies)}")
    
    def save(self) -> None:
        """
        Sauvegarde la configuration actuelle dans le fichier JSON
        """
        try:
            # Création du dictionnaire de configuration à partir des attributs de l'instance
            config_to_save = {key: getattr(self, key) for key in self.DEFAULT_CONFIG.keys() 
                            if hasattr(self, key)}
            
            # Sauvegarde dans le fichier
            with open(self.config_path, 'w') as config_file:
                json.dump(config_to_save, config_file, indent=4)
            
            self.logger.info(f"Configuration sauvegardée dans {self.config_path}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
    
    def update(self, new_config: Dict[str, Any]) -> None:
        """
        Met à jour la configuration avec de nouvelles valeurs
        
        :param new_config: Dictionnaire contenant les nouvelles valeurs de configuration
        """
        for key, value in new_config.items():
            if key in self.DEFAULT_CONFIG:
                setattr(self, key, value)
                self.config_data[key] = value
            else:
                self.logger.warning(f"Clé de configuration inconnue: {key}")
        
        # Sauvegarde des changements
        self.save()
        self.logger.info("Configuration mise à jour")

# Pour tester le module directement
if __name__ == "__main__":
    # Configuration du logger
    logging.basicConfig(level=logging.INFO, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Test de chargement de la configuration
    config = Config()
    print("Configuration chargée:")
    for key, value in config.config_data.items():
        print(f"{key}: {value}")
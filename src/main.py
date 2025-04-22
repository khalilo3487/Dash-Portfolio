#!/usr/bin/env python3
"""
main.py - Point d'entrée principal du bot HFT pour le trading de cryptomonnaies sur Binance
"""
import os
import sys
import time
import signal
import argparse
import logging
from datetime import datetime

# Import des modules internes
from config import Config
from api.binance_client import BinanceClient
from strategies.hft_strategies import MarketMakingStrategy, ArbitrageStrategy, MomentumStrategy
from execution.order_manager import OrderManager
from risk.risk_manager import RiskManager
from utils.logger import setup_logger
from utils.performance_tracker import PerformanceTracker
from database.db_manager import DatabaseManager
from notification.alert_system import AlertSystem

# Variables globales
running = True

def signal_handler(sig, frame):
    """Gestionnaire pour l'arrêt gracieux du bot"""
    global running
    print("\nArrêt du bot en cours... Veuillez patienter.")
    running = False

def parse_arguments():
    """Parse les arguments de ligne de commande"""
    parser = argparse.ArgumentParser(description='Bot HFT pour trading de cryptomonnaies sur Binance')
    parser.add_argument('--config', type=str, default='config.json', help='Chemin vers le fichier de configuration')
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    parser.add_argument('--backtest', action='store_true', help='Mode backtest (pas de trading réel)')
    parser.add_argument('--strategy', type=str, default='market_making', 
                        choices=['market_making', 'arbitrage', 'momentum'],
                        help='Stratégie à utiliser')
    return parser.parse_args()

def initialize_components(config, logger):
    """Initialise tous les composants du bot"""
    logger.info("Initialisation des composants du bot...")
    
    # Initialisation de la connexion à l'API Binance
    binance_client = BinanceClient(
        api_key=config.API_KEY,
        api_secret=config.API_SECRET,
        testnet=config.USE_TESTNET,
        logger=logger
    )
    
    # Vérification de la connexion
    account_info = binance_client.get_account_info()
    logger.info(f"Connecté au compte Binance: {account_info['accountType']}")
    
    # Initialisation de la base de données
    db_manager = DatabaseManager(
        db_path=config.DB_PATH,
        logger=logger
    )
    
    # Initialisation du système d'alertes
    alert_system = AlertSystem(
        email_config=config.EMAIL_CONFIG,
        telegram_config=config.TELEGRAM_CONFIG,
        logger=logger
    )
    
    # Initialisation du gestionnaire de risques
    risk_manager = RiskManager(
        max_position_size=config.MAX_POSITION_SIZE,
        max_risk_per_trade=config.MAX_RISK_PER_TRADE,
        max_daily_loss=config.MAX_DAILY_LOSS,
        logger=logger
    )
    
    # Initialisation du gestionnaire d'ordres
    order_manager = OrderManager(
        binance_client=binance_client,
        risk_manager=risk_manager,
        logger=logger
    )
    
    # Initialisation du suivi de performance
    performance_tracker = PerformanceTracker(
        db_manager=db_manager,
        logger=logger
    )
    
    # Initialisation de la stratégie choisie
    if config.STRATEGY == 'market_making':
        strategy = MarketMakingStrategy(
            symbol=config.SYMBOL,
            spread=config.MM_SPREAD,
            order_size=config.MM_ORDER_SIZE,
            binance_client=binance_client,
            order_manager=order_manager,
            logger=logger
        )
    elif config.STRATEGY == 'arbitrage':
        strategy = ArbitrageStrategy(
            symbols=config.ARBITRAGE_SYMBOLS,
            min_profit_threshold=config.MIN_PROFIT_THRESHOLD,
            binance_client=binance_client,
            order_manager=order_manager,
            logger=logger
        )
    elif config.STRATEGY == 'momentum':
        strategy = MomentumStrategy(
            symbol=config.SYMBOL,
            timeframe=config.MOMENTUM_TIMEFRAME,
            lookback_period=config.LOOKBACK_PERIOD,
            binance_client=binance_client,
            order_manager=order_manager,
            logger=logger
        )
    else:
        raise ValueError(f"Stratégie non reconnue: {config.STRATEGY}")
    
    return {
        'binance_client': binance_client,
        'db_manager': db_manager,
        'alert_system': alert_system,
        'risk_manager': risk_manager,
        'order_manager': order_manager,
        'performance_tracker': performance_tracker,
        'strategy': strategy
    }

def main():
    """Fonction principale du bot"""
    # Capture des signaux pour arrêt gracieux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse des arguments
    args = parse_arguments()
    
    # Configuration du logger
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = setup_logger(log_level=log_level)
    
    # Chargement de la configuration
    logger.info("Chargement de la configuration...")
    config = Config(config_path=args.config)
    
    # Mode backtest ou trading réel
    if args.backtest:
        logger.info("Mode BACKTEST activé - Aucun ordre réel ne sera passé")
        config.USE_TESTNET = True
    
    # Initialisation des composants
    components = initialize_components(config, logger)
    
    # Message de démarrage
    logger.info("=" * 50)
    logger.info(f"Démarrage du bot HFT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Stratégie: {config.STRATEGY}")
    logger.info(f"Symbole principal: {config.SYMBOL}")
    logger.info("=" * 50)
    
    # Boucle principale
    try:
        while running:
            # Mise à jour des données de marché
            market_data = components['binance_client'].get_market_data(config.SYMBOL)
            
            # Exécution de la stratégie
            signals = components['strategy'].generate_signals(market_data)
            
            # Traitement des signaux
            if signals:
                for signal in signals:
                    components['order_manager'].process_signal(signal)
            
            # Suivi des performances
            components['performance_tracker'].update()
            
            # Vérification des alertes
            components['alert_system'].check_conditions()
            
            # Pause pour ne pas dépasser les limites de l'API
            time.sleep(config.LOOP_INTERVAL)
            
    except Exception as e:
        logger.error(f"Erreur critique: {str(e)}", exc_info=True)
        components['alert_system'].send_alert("Erreur critique", str(e))
    
    finally:
        # Nettoyage et fermeture propre
        logger.info("Fermeture des connexions et sauvegarde de l'état...")
        components['binance_client'].close()
        components['db_manager'].save_state()
        logger.info("Bot arrêté avec succès.")

if __name__ == "__main__":
    main()
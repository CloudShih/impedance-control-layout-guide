"""
Main entry point for the Impedance Control Layout Guide Generator.
整合所有模組的主要程式入口
"""
from pathlib import Path
from typing import Optional
import logging
import sys

# Add src to path for imports
# Handle both development and PyInstaller environments
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Running in PyInstaller bundle
    sys.path.insert(0, str(Path(sys._MEIPASS) / "src"))
else:
    # Running in development
    sys.path.insert(0, str(Path(__file__).parent))

from core.netlist_parser import NetlistParser
from core.net_classifier import NetClassifier  
from core.rule_engine import RuleEngine
from core.template_mapper import TemplateMapper
from config.config_manager import ConfigManager


def setup_logging(config_manager: ConfigManager) -> None:
    """Set up logging configuration."""
    log_config = config_manager.get_section('logging')
    
    level = getattr(logging, log_config.get('level', 'INFO'))
    format_str = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
    
    # Create logs directory if it doesn't exist
    log_file_path = Path(log_config.get('log_file_path', 'logs/impedance_tool.log'))
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    handlers = []
    
    if log_config.get('console_output', True):
        handlers.append(logging.StreamHandler())
    
    if log_config.get('file_output', True):
        handlers.append(logging.FileHandler(log_file_path, encoding='utf-8'))
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=handlers
    )


def process_netlist_to_excel(netlist_path: Path, 
                            template_path: Optional[Path] = None,
                            output_path: Optional[Path] = None,
                            config_path: Optional[Path] = None) -> Path:
    """
    Complete pipeline from netlist to Excel output.
    
    Args:
        netlist_path: Path to netlist file
        template_path: Path to Excel template (optional)
        output_path: Path for output Excel file (optional)
        config_path: Path to configuration file (optional)
        
    Returns:
        Path to generated Excel file
    """
    # Load configuration
    config_manager = ConfigManager(config_path)
    config = config_manager.load_config()
    
    # Setup logging
    setup_logging(config_manager)
    logger = logging.getLogger(__name__)
    
    logger.info("=== 阻抗控制佈局指南生成開始 ===")
    logger.info(f"處理 Netlist 檔案: {netlist_path}")
    
    try:
        # Step 1: Parse netlist
        logger.info("步驟 1: 解析 Netlist 檔案")
        parser_config = config_manager.get_section('netlist_parser')
        parser = NetlistParser(parser_config)
        net_names = parser.parse(netlist_path)
        logger.info(f"提取到 {len(net_names)} 個網路名稱")
        
        # Step 2: Classify nets
        logger.info("步驟 2: 分類網路名稱")
        classifier = NetClassifier(config)
        classified_nets = classifier.classify(net_names)
        
        # Log classification summary
        summary = classifier.get_classification_summary(classified_nets)
        for category, count in summary.items():
            logger.info(f"  {category}: {count} 個網路")
        
        # Step 3: Apply layout rules
        logger.info("步驟 3: 應用佈局規則")
        rule_engine = RuleEngine(config)
        layout_data = rule_engine.apply_rules(classified_nets)
        
        # Step 4: Map to Excel template
        logger.info("步驟 4: 生成 Excel 檔案")
        template_mapper = TemplateMapper(config)
        output_file = template_mapper.map_to_template(
            layout_data, 
            template_path, 
            output_path
        )
        
        logger.info(f"=== 處理完成! 輸出檔案: {output_file} ===")
        return output_file
        
    except Exception as e:
        logger.error(f"處理過程中發生錯誤: {str(e)}")
        raise


def main():
    """Main function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="阻抗控制佈局指南生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例用法:
  python main.py netlist.net
  python main.py netlist.net -o output.xlsx
  python main.py netlist.net -c custom_config.yaml
        """
    )
    
    parser.add_argument('netlist', type=Path, help='Netlist 檔案路徑')
    parser.add_argument('-t', '--template', type=Path, help='Excel 模板檔案路徑')
    parser.add_argument('-o', '--output', type=Path, help='輸出 Excel 檔案路徑')
    parser.add_argument('-c', '--config', type=Path, help='配置檔案路徑')
    
    args = parser.parse_args()
    
    try:
        output_file = process_netlist_to_excel(
            netlist_path=args.netlist,
            template_path=args.template,
            output_path=args.output,
            config_path=args.config
        )
        print(f"✅ 成功生成佈局指南: {output_file}")
        
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
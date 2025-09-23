#!/usr/bin/env python3 #DEEPSEEK
"""
🤖 PURE LOCAL AI AUTOMATION SYSTEM
Advanced Browser Automation + System Control + AI Assistant
No Telegram - Pure Local Execution
"""

import os
import sys
import json
import time
import uuid
import logging
import threading
import subprocess
import platform
from queue import Queue, Empty
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# ===== AUTO-INSTALL DEPENDENCIES =====
def install_dependencies():
    """Automatically install required packages"""
    required_packages = [
        "browser-use", 
        "selenium", 
        "webdriver-manager", 
        "psutil"
    ]
    
    for package in required_packages:
        try:
            if package == "browser-use":
                __import__("browser_use")
            elif package == "webdriver-manager":
                __import__("webdriver_manager")
            elif package == "selenium":
                __import__("selenium")
            elif package == "psutil":
                __import__("psutil")
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install dependencies on startup
install_dependencies()

# ===== NOW IMPORT EVERYTHING =====
from browser_use import Agent, Browser
from browser_use.llm import ChatGoogle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import psutil

# ===== CONFIGURATION =====
class Config:
    # API Key (Directly embedded - no .env needed)
    GEMINI_API_KEY = "AIzaSyDnsQ_EaKER5TghXoh8mpkoy_tXZoaYZ58"
    
    # System Settings
    MODEL = "gemini-2.5-flash"
    MAX_WORKERS = 2
    TASK_TIMEOUT = 600  # 10 minutes
    HEADLESS = False  # Show browser for visibility
    
    # Paths
    BASE_DIR = Path.home() / "AI_Automation_System"
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    DOWNLOADS_DIR = BASE_DIR / "downloads"
    
    # Automation Settings
    TYPING_DELAY = 0.05
    SCROLL_DELAY = 0.5
    WAIT_TIMEOUT = 30

# ===== ADVANCED LOGGING SYSTEM =====
class AdvancedLogger:
    def __init__(self):
        self.setup_directories()
        self.setup_logging()
    
    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            Config.BASE_DIR,
            Config.LOGS_DIR,
            Config.DATA_DIR,
            Config.SCREENSHOTS_DIR,
            Config.DOWNLOADS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logger = logging.getLogger("AI_Automation_System")
        logger.setLevel(logging.INFO)
        
        # File handler
        log_file = Config.LOGS_DIR / f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        self.logger = logger

# ===== AI AGENT MANAGER =====
class AIAgentManager:
    def __init__(self):
        self.logger = AdvancedLogger().logger
        self.agents = {}
        self.active_tasks = {}
        
    def create_agent(self, agent_id="default"):
        """Create a new AI agent with browser capabilities"""
        try:
            # Setup Chrome browser with advanced options
            service = Service(ChromeDriverManager().install())
            
            chrome_options = webdriver.ChromeOptions()
            if not Config.HEADLESS:
                chrome_options.add_argument("--start-maximized")
            else:
                chrome_options.add_argument("--headless")
                
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set download directory
            prefs = {
                "download.default_directory": str(Config.DOWNLOADS_DIR),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Create browser instance
            browser = Browser(
                headless=Config.HEADLESS,
                service=service,
                options=chrome_options
            )
            
            # Create AI agent
            llm = ChatGoogle(model=Config.MODEL, api_key=Config.GEMINI_API_KEY)
            agent = Agent(
                task="Ready for automation tasks",
                llm=llm,
                browser=browser
            )
            
            self.agents[agent_id] = agent
            self.logger.info(f"🤖 Agent '{agent_id}' created successfully")
            return agent
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create agent: {e}")
            return None

    def execute_task(self, task_description, agent_id="default"):
        """Execute a task with the AI agent"""
        task_id = str(uuid.uuid4())[:8]
        self.active_tasks[task_id] = {
            "status": "running",
            "start_time": datetime.now(),
            "description": task_description
        }
        
        try:
            if agent_id not in self.agents:
                self.create_agent(agent_id)
            
            agent = self.agents[agent_id]
            agent.task = f"""
            Perform this task in the browser step by step: {task_description}
            
            Important instructions:
            - Don't close the browser after completing tasks
            - Keep sessions alive for follow-up tasks
            - Take your time and be thorough
            - If you encounter errors, try alternative approaches
            - Report what you accomplished
            """
            
            self.logger.info(f"🚀 Starting task {task_id}: {task_description}")
            print(f"🤖 AI: 'Working on: {task_description}'")
            
            result = agent.run_sync(timeout=Config.TASK_TIMEOUT)
            
            self.active_tasks[task_id].update({
                "status": "completed",
                "end_time": datetime.now(),
                "result": str(result)
            })
            
            self.logger.info(f"✅ Task {task_id} completed successfully")
            return result
            
        except Exception as e:
            self.active_tasks[task_id].update({
                "status": "failed",
                "end_time": datetime.now(),
                "error": str(e)
            })
            self.logger.error(f"❌ Task {task_id} failed: {e}")
            return f"Task failed: {e}"

# ===== SYSTEM COMMAND EXECUTOR =====
class SystemCommandExecutor:
    def __init__(self):
        self.logger = AdvancedLogger().logger
    
    def execute_command(self, command, timeout=60):
        """Execute system commands safely"""
        try:
            self.logger.info(f"💻 Executing: {command}")
            
            # Determine shell based on platform
            shell = True if platform.system() == "Windows" else True
            
            result = subprocess.run(
                command, 
                shell=shell, 
                timeout=timeout,
                capture_output=True, 
                text=True,
                cwd=str(Config.BASE_DIR)
            )
            
            output = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
            if result.returncode == 0:
                self.logger.info(f"✅ Command executed successfully")
            else:
                self.logger.warning(f"⚠️ Command completed with return code: {result.returncode}")
            
            return output
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout} seconds"
            self.logger.error(f"⏰ {error_msg}")
            return {"success": False, "error": error_msg}
        except Exception as e:
            self.logger.error(f"❌ Command execution failed: {e}")
            return {"success": False, "error": str(e)}

# ===== FILE SYSTEM MANAGER =====
class FileSystemManager:
    def __init__(self):
        self.logger = AdvancedLogger().logger
    
    def read_file(self, file_path):
        """Read any file with automatic encoding detection"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {"success": False, "error": f"File not found: {file_path}"}
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(path, 'r', encoding=encoding) as f:
                        content = f.read()
                    return {"success": True, "content": content, "encoding": encoding}
                except UnicodeDecodeError:
                    continue
            
            # If text reading fails, return binary
            with open(path, 'rb') as f:
                content = f.read()
            return {"success": True, "content": content, "binary": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, file_path, content):
        """Write content to file with backup"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create backup if file exists
            if path.exists():
                timestamp = int(time.time())
                backup_path = path.with_suffix(f'.backup_{timestamp}{path.suffix}')
                path.rename(backup_path)
                self.logger.info(f"📦 Backup created: {backup_path}")
            
            # Write the file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"💾 File saved: {path}")
            return {"success": True, "path": str(path), "size": len(content)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_directory(self, directory="."):
        """List directory contents with details"""
        try:
            path = Path(directory)
            if not path.exists():
                return {"success": False, "error": f"Directory not found: {directory}"}
            
            contents = []
            for item in path.iterdir():
                stat = item.stat()
                item_info = {
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "path": str(item)
                }
                contents.append(item_info)
            
            return {"success": True, "path": str(path), "contents": contents}
        except Exception as e:
            return {"success": False, "error": str(e)}

# ===== MAIN AI ASSISTANT =====
class UltimateAIAssistant:
    def __init__(self):
        self.logger = AdvancedLogger().logger
        self.agent_manager = AIAgentManager()
        self.command_executor = SystemCommandExecutor()
        self.file_manager = FileSystemManager()
        
        self.conversation_history = []
        self.session_id = str(uuid.uuid4())[:8]
        
        self.show_welcome_message()
        self.logger.info(f"🚀 AI Assistant Session Started: {self.session_id}")
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(str(Config.BASE_DIR))
            
            return {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "cpu_count": os.cpu_count(),
                "memory_total_gb": round(memory.total / (1024**3), 1),
                "memory_available_gb": round(memory.available / (1024**3), 1),
                "memory_used_percent": memory.percent,
                "disk_free_gb": round(disk.free / (1024**3), 1),
                "disk_used_percent": disk.percent,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Could not get system info: {e}"}
    
    def show_welcome_message(self):
        """Display awesome welcome message"""
        system_info = self.get_system_info()
        
        print("=" * 70)
        print("🤖 ULTIMATE AI AUTOMATION SYSTEM - LOCAL EDITION")
        print("=" * 70)
        print(f"📁 Workspace: {Config.BASE_DIR}")
        print(f"💻 Platform: {system_info['platform']}")
        print(f"🐍 Python: {system_info['python_version']}")
        print(f"🧠 AI Model: {Config.MODEL}")
        print(f"💾 Memory: {system_info['memory_available_gb']}GB available")
        print(f"💿 Disk: {system_info['disk_free_gb']}GB free")
        print("=" * 70)
        print("🎯 AVAILABLE COMMANDS:")
        print("  • [task] - AI will automatically determine the best approach")
        print("  • browser [task] - Force browser automation")
        print("  • system [command] - Execute system commands")
        print("  • file [action] - File operations")
        print("  • status - System status")
        print("  • clear - Clear screen")
        print("  • help - Show detailed help")
        print("  • exit - Quit application")
        print("=" * 70)
        print("💡 Examples: 'search for AI news', 'system dir', 'file list .'")
        print("=" * 70)
    
    def process_command(self, user_input):
        """Process user commands with smart routing"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Please enter a command"
        
        # Add to conversation history
        self.conversation_history.append({
            "user": user_input, 
            "timestamp": datetime.now().isoformat()
        })
        
        # Command routing
        if user_input.lower().startswith('browser '):
            task = user_input[8:].strip()
            return self.handle_browser_task(task)
        
        elif user_input.lower().startswith('system '):
            command = user_input[7:].strip()
            return self.handle_system_command(command)
        
        elif user_input.lower().startswith('file '):
            action = user_input[5:].strip()
            return self.handle_file_action(action)
        
        elif user_input.lower() == 'status':
            return self.handle_status()
        
        elif user_input.lower() == 'clear':
            os.system('cls' if platform.system() == 'Windows' else 'clear')
            return "Screen cleared!"
        
        elif user_input.lower() in ['help', '?']:
            return self.show_help()
        
        elif user_input.lower() in ['exit', 'quit']:
            return self.shutdown()
        
        else:
            # Default: AI determines best approach
            return self.handle_ai_task(user_input)
    
    def handle_ai_task(self, task_description):
        """Let AI determine the best approach for the task"""
        self.logger.info(f"🤖 AI Task: {task_description}")
        
        # For certain tasks, use specific handlers
        if any(keyword in task_description.lower() for keyword in [
            'search', 'browse', 'website', 'web', 'google', 'youtube', 'login'
        ]):
            return self.handle_browser_task(task_description)
        elif any(keyword in task_description.lower() for keyword in [
            'run', 'execute', 'command', 'install', 'update', 'python'
        ]):
            return self.handle_system_command(task_description)
        elif any(keyword in task_description.lower() for keyword in [
            'read', 'write', 'file', 'folder', 'directory', 'list'
        ]):
            return self.handle_file_action(task_description)
        else:
            # Default to browser automation
            return self.handle_browser_task(task_description)
    
    def handle_browser_task(self, task_description):
        """Handle browser automation tasks"""
        if not task_description:
            return "❌ Please provide a task description"
        
        print(f"🌐 Browser Automation: '{task_description}'")
        print("🤖 AI is working on it...")
        
        try:
            result = self.agent_manager.execute_task(task_description)
            return f"✅ Task Completed!\n\n📋 Result:\n{result}"
            
        except Exception as e:
            return f"❌ Browser task failed:\n{str(e)}"
    
    def handle_system_command(self, command):
        """Handle system command execution"""
        if not command:
            return "❌ Please provide a command"
        
        result = self.command_executor.execute_command(command)
        
        if result['success']:
            output = result['stdout'] or "Command executed successfully"
            return f"✅ System Command Executed!\n\n📤 Output:\n{output}"
        else:
            error = result.get('error') or result.get('stderr') or "Unknown error"
            return f"❌ Command Failed:\n{error}"
    
    def handle_file_action(self, action):
        """Handle file system operations"""
        parts = action.split(' ', 1)
        operation = parts[0].lower()
        
        if operation == 'read' and len(parts) > 1:
            file_path = parts[1]
            result = self.file_manager.read_file(file_path)
            if result['success']:
                content = result['content']
                if isinstance(content, str):
                    preview = content[:1000] + "..." if len(content) > 1000 else content
                    return f"📖 File Content ({result.get('encoding', 'binary')}):\n{preview}"
                else:
                    return f"📁 Binary file: {len(content)} bytes"
            else:
                return f"❌ Error reading file: {result['error']}"
        
        elif operation == 'write' and len(parts) > 1:
            # Simple write operation
            write_parts = parts[1].split(' ', 1)
            if len(write_parts) < 2:
                return "❌ Usage: file write [filename] [content]"
            
            filename, content = write_parts
            result = self.file_manager.write_file(filename, content)
            if result['success']:
                return f"✅ File written: {result['path']} ({result['size']} bytes)"
            else:
                return f"❌ Error writing file: {result['error']}"
        
        elif operation == 'list':
            path = parts[1] if len(parts) > 1 else "."
            result = self.file_manager.list_directory(path)
            if result['success']:
                items = result['contents']
                if not items:
                    return f"📁 Directory is empty: {result['path']}"
                
                output = []
                for item in items[:20]:  # Show first 20 items
                    size = f"{item['size']} bytes" if item['type'] == 'file' else "DIR"
                    output.append(f"  {item['type'][0].upper()}: {item['name']} ({size})")
                
                listing = "\n".join(output)
                if len(items) > 20:
                    listing += f"\n  ... and {len(items) - 20} more items"
                
                return f"📁 Directory: {result['path']}\n{listing}"
            else:
                return f"❌ Error listing directory: {result['error']}"
        
        else:
            return "❌ Unknown file operation. Use: read, write, or list"
    
    def handle_status(self):
        """Display comprehensive system status"""
        system_info = self.get_system_info()
        
        status_lines = [
            f"🕒 System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"📁 Workspace: {Config.BASE_DIR}",
            f"🐍 Python: {system_info['python_version']}",
            f"🧠 AI Model: {Config.MODEL}",
            f"🤖 Active Agents: {len(self.agent_manager.agents)}",
            f"📊 Active Tasks: {len(self.agent_manager.active_tasks)}",
            f"💾 Memory: {system_info['memory_available_gb']}GB available ({system_info['memory_used_percent']}% used)",
            f"💿 Disk: {system_info['disk_free_gb']}GB free ({system_info['disk_used_percent']}% used)",
            f"📝 Session ID: {system_info['session_id']}",
            f"💬 Commands this session: {len(self.conversation_history)}"
        ]
        
        return "\n".join(status_lines)
    
    def show_help(self):
        """Display comprehensive help information"""
        help_text = """
🤖 ULTIMATE AI ASSISTANT - COMMAND REFERENCE

🎯 SMART TASK EXECUTION:
  Simply describe what you want - AI will choose the best approach
  Examples:
    - "search for latest AI news on Google"
    - "check the weather forecast"
    - "research Python web scraping tutorials"

🌐 BROWSER AUTOMATION:
  • browser [task] - Force browser automation
  Examples:
    - "browser login to Gmail and check emails"
    - "browser search for Python documentation"
    - "browser fill out contact form on example.com"

💻 SYSTEM COMMANDS:
  • system [command] - Execute system commands
  Examples:
    - "system dir" (Windows) or "system ls -la" (Linux/Mac)
    - "system python --version"
    - "system pip list --outdated"

📁 FILE OPERATIONS:
  • file read [path] - Read file content
  • file write [path] [content] - Write to file
  • file list [path] - List directory contents

🔧 UTILITY COMMANDS:
  • status - Show system status
  • clear - Clear the screen
  • help - Show this help
  • exit - Quit the application

💡 PRO TIPS:
  - Be specific for better results
  - The AI can handle complex multi-step tasks
  - All actions are logged for review
  - Browser sessions are kept alive for follow-up tasks
        """
        return help_text
    
    def shutdown(self):
        """Clean shutdown procedure"""
        self.logger.info("🛑 Shutting down AI Assistant...")
        
        # Close all browser instances
        for agent_id, agent in self.agent_manager.agents.items():
            try:
                agent.browser.close()
                self.logger.info(f"✅ Closed browser for agent {agent_id}")
            except Exception as e:
                self.logger.error(f"❌ Error closing browser {agent_id}: {e}")
        
        # Save session history
        session_file = Config.DATA_DIR / f"session_{self.session_id}.json"
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_id": self.session_id,
                    "start_time": self.conversation_history[0]['timestamp'] if self.conversation_history else datetime.now().isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "total_commands": len(self.conversation_history),
                    "commands": self.conversation_history
                }, f, indent=2)
            self.logger.info(f"💾 Session saved: {session_file}")
        except Exception as e:
            self.logger.error(f"❌ Error saving session: {e}")
        
        return "SHUTDOWN"

# ===== MAIN EXECUTION =====
def main():
    """Main execution function"""
    try:
        assistant = UltimateAIAssistant()
        
        # Main interaction loop
        while True:
            try:
                user_input = input("\n🎯 You: ").strip()
                
                if not user_input:
                    continue
                
                result = assistant.process_command(user_input)
                
                if result == "SHUTDOWN":
                    print("\n👋 Thank you for using Ultimate AI Assistant!")
                    break
                
                print(f"\n🤖 AI Assistant:\n{result}")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Press Ctrl+C again to exit, or type 'exit' to quit properly.")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                assistant.logger.error(f"Unexpected error in main loop: {e}")
    
    except Exception as e:
        print(f"💥 Critical error during startup: {e}")
        print("Please check your Python installation and try again.")

if __name__ == "__main__":
    main()

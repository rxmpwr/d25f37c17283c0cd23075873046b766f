"""
Localization Script - Dịch giao diện YouTube Analyzer Pro sang tiếng Việt
Version 2.0 - Chỉ dịch text UI, không dịch code
"""

import os
import re
from typing import Dict, List, Tuple

# Dictionary chứa các cụm từ cần dịch
TRANSLATIONS = {
    # Main Window & Titles
    "Viral YouTube Analyzer Pro": "Viral Youtube Content Creator",
    "YouTube Analyzer Pro": "Viral Youtube Content Creator",
    "Analyze YouTube content → Customize prompts → Generate viral stories": "Phân tích nội dung YouTube → Tùy chỉnh prompts → Tạo câu chuyện viral",
    
    # Tab Names (chỉ trong strings)
    "🎯 Input Configuration": "🎯 Cấu Hình Đầu Vào", 
    "📊 Analysis Result": "📊 Kết Quả Phân Tích",
    "✏️ Create Prompts": "✏️ Tạo Prompts",
    "💡 Generate Topic": "💡 Tạo Chủ Đề",
    "📝 Generate Content": "📝 Tạo Nội Dung",
    "⚙️ Settings": "⚙️ Cài Đặt",
    
    # Messages trong messagebox
    "API Configuration": "Cấu Hình API",
    "Would you like to configure API keys now?": "Bạn có muốn cấu hình API keys ngay bây giờ?",
    "Startup Error": "Lỗi Khởi Động",
    "Failed to start YouTube Analyzer Pro": "Không thể khởi động Youtube Analyzer Pro",
    "Failed to start application": "Không thể khởi động ứng dụng",
    
    # Input Tab UI Text
    "YouTube URL Input": "Nhập URL Youtube",
    "Analysis Mode:": "Chế độ phân tích:",
    "Channel Analysis": "Phân tích kênh",
    "Video List Analysis": "Phân tích danh sách video",
    "📺 Enter YouTube Channel URLs (analyzes latest videos from each channel):": "📺 Nhập URL kênh Youtube (phân tích video mới nhất từ mỗi kênh):",
    "🎯 Custom Analysis Requirements (Optional):": "🎯 Yêu Cầu Phân Tích Tùy Chỉnh (Tùy chọn):",
    "Describe what specific insights you want from the analysis. Leave empty for comprehensive analysis.": "Mô tả những insights cụ thể bạn muốn từ phân tích. Để trống cho phân tích toàn diện.",
    "Quick templates:": "Mẫu nhanh:",
    "Viral Analysis": "Phân Tích Viral", 
    "Audience Insights": "Thông Tin Khán Giả",
    "Content Strategy": "Chiến Lược Nội Dung",
    "Competitor Analysis": "Phân Tích Đối Thủ",
    
    # Buttons
    "🗑️ Clear All URLs": "🗑️ Xóa Tất Cả URLs",
    "✓ Validate URLs": "✓ Kiểm Tra URLs", 
    "📋 Load Sample URLs": "📋 Tải URLs Mẫu",
    "🔍 Analyze": "🔍 Phân Tích",
    
    # Labels
    "Max videos (per channel):": "Số video tối đa (mỗi kênh):",
    "Max comments (per video):": "Số bình luận tối đa (mỗi video):",
    "✓ Include transcript": "✓ Bao gồm phụ đề",
    "✓ Include comments": "✓ Bao gồm bình luận",
    " URLs entered": " URLs đã nhập",
    
    # Analysis Tab
    "📊 Analysis Results": "📊 Kết Quả Phân Tích",
    "🔄 Analysis in Progress...": "🔄 Đang Phân Tích...",
    "Analyzing YouTube data. This may take a few minutes...": "Đang phân tích dữ liệu Youtube. Quá trình này có thể mất vài phút...",
    "⏱️ Time Elapsed:": "⏱️ Thời gian đã qua:",
    "📹 Videos Analyzed:": "📹 Video đã phân tích:",
    "💬 Comments Collected:": "💬 Bình luận đã thu thập:",
    "📄 Transcripts Collected:": "📄 Phụ đề đã thu thập:",
    "🎯 Current Task:": "🎯 Tác vụ hiện tại:",
    "✅ Analysis Complete!": "✅ Phân Tích Hoàn Tất!",
    "🎉 Viral Score:": "🎉 Điểm Viral:",
    "📊 Total Videos:": "📊 Tổng số video:",
    "💬 Total Comments:": "💬 Tổng bình luận:",
    "📄 Total Transcripts:": "📄 Tổng phụ đề:",
    "👁️ Total Views:": "👁️ Tổng lượt xem:",
    "❤️ Total Likes:": "❤️ Tổng lượt thích:",
    "🎯 Additional Analysis Requirements": "🎯 Yêu Cầu Phân Tích Bổ Sung",
    "Enter additional requirements for AI analysis...": "Nhập yêu cầu bổ sung cho phân tích AI...",
    "📥 Export JSON": "📥 Xuất JSON",
    "📊 Export CSV": "📊 Xuất CSV", 
    "✏️ Create Prompts →": "✏️ Tạo Prompts →",
    
    # Messages and Errors
    "No URLs": "Không có URLs",
    "Please enter at least one YouTube URL.": "Vui lòng nhập ít nhất một URL Youtube.",
    "Invalid URLs Found": "Tìm thấy URLs không hợp lệ",
    "Continue with valid URLs only?": "Tiếp tục với URLs hợp lệ?",
    "No Valid URLs": "Không có URLs hợp lệ",
    "No valid YouTube URLs found.": "Không tìm thấy URLs Youtube hợp lệ.",
    "Invalid Parameters": "Tham số không hợp lệ",
    "Max videos and comments must be numbers.": "Số video và bình luận tối đa phải là số.",
    "Validation Result": "Kết quả kiểm tra",
    "All": "Tất cả",
    "URLs are valid! ✅": "URLs hợp lệ! ✅",
    "Valid URLs:": "URLs hợp lệ:",
    "Invalid URLs:": "URLs không hợp lệ:",
    
    # Settings Tab
    "🔐 API Configuration": "🔐 Cấu Hình API",
    "🎬 YouTube API Keys": "🎬 Youtube API Key",
    "Add multiple keys for quota rotation": "Thêm nhiều khóa để xoay vòng hạn mức",
    "➕ Add Key": "➕ Thêm API Key",
    "🧠 OpenAI API Keys": "🧠 OpenAI API Key", 
    "🎨 Leonardo AI Key": "🎨 Leonardo AI Key",
    "📄 Google Service Account": "📄 Tài khoản dịch vụ Google",
    "🔧 Generation Settings": "🔧 Cài Đặt Tạo Nội Dung",
    "Viral Threshold:": "Ngưỡng Viral:",
    "Quality:": "Chất lượng:",
    "Balanced": "Cân bằng",
    "High Quality": "Chất lượng cao", 
    "Fast": "Nhanh",
    "Enable Viral Scoring": "Bật tính điểm viral",
    "Enable Retry on Failure": "Bật thử lại khi thất bại",
    "Auto Optimize Results": "Tự động tối ưu kết quả",
    "💾 Save Settings": "💾 Lưu Cài Đặt",
    "🔍 Test All APIs": "🔍 Kiểm Tra Tất Cả APIs",
    "📊 API Status": "📊 Trạng thái API",
    
    # API Status Messages  
    "API Keys Required": "Cần có API key",
    "Please configure your API keys in the Settings tab.": "Vui lòng cấu hình API key trong tab Cài Đặt.",
    "No YouTube API Keys": "Không có khóa YouTube API Key",
    "Please add at least one YouTube API key in Settings tab.": "Vui lòng thêm ít nhất một Youtube API key trong tab Cài Đặt.",
    "Missing Dependencies": "Thiếu thư viện phụ thuộc",
    "YouTube integration module not available!": "Module tích hợp Youtube không khả dụng!",
    "Please install required packages:": "Vui lòng cài đặt các gói cần thiết:",
    "Analysis Error": "Lỗi phân tích",
    "Failed to start analysis:": "Không thể bắt đầu phân tích:",
    
    # Export Messages
    "Success": "Thành công",
    "Data exported to:": "Dữ liệu đã xuất ra:",
    "Export Error": "Lỗi xuất file",
    "Failed to export data:": "Không thể xuất dữ liệu:",
    "No Data": "Không có dữ liệu",
    "No video data to export!": "Không có dữ liệu video để xuất!",
    
    # Progress Messages
    "Initializing...": "Đang khởi tạo...",
    "Collecting channel data...": "Thu thập dữ liệu kênh...",
    "Fetching video details...": "Lấy chi tiết video...",
    "Collecting transcripts...": "Thu thập phụ đề...",
    "Analyzing comments...": "Phân tích bình luận...",
    "Generating insights...": "Tạo insights...",
    "Calculating viral score...": "Tính điểm viral...",
}

def translate_file_safely(file_path: str) -> bool:
    """Translate a file safely - only UI text, not code."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            new_line = line
            
            # Skip import statements and code logic
            if line.strip().startswith(('import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', 'return ', 'raise ')):
                new_lines.append(line)
                continue
            
            # Translate text in specific patterns only
            patterns_to_translate = [
                # CTkLabel text
                (r'text="([^"]+)"', 'text'),
                (r"text='([^']+)'", 'text'),
                
                # Window titles
                (r'\.title\("([^"]+)"\)', 'title'),
                (r"\.title\('([^']+)'\)", 'title'),
                
                # Messagebox
                (r'messagebox\.\w+\("([^"]+)",\s*"([^"]+)"', 'messagebox'),
                (r"messagebox\.\w+\('([^']+)',\s*'([^']+)'", 'messagebox'),
                
                # CTkButton text
                (r'CTkButton\([^)]*text="([^"]+)"', 'button'),
                (r"CTkButton\([^)]*text='([^']+)'", 'button'),
                
                # configure text
                (r'\.configure\([^)]*text="([^"]+)"', 'configure'),
                (r"\.configure\([^)]*text='([^']+)'", 'configure'),
                
                # Tab names in tuples
                (r'\("(\w+)",\s*"([^"]+)",\s*\d+\)', 'tab_tuple'),
                
                # Logging and print statements
                (r'logger\.\w+\("([^"]+)"\)', 'logger'),
                (r'print\("([^"]+)"\)', 'print'),
                (r"print\('([^']+)'\)", 'print'),
                
                # f-strings with simple content
                (r'f"([^{]+)"', 'fstring_simple'),
                (r"f'([^{]+)'", 'fstring_simple'),
            ]
            
            for pattern, pattern_type in patterns_to_translate:
                matches = list(re.finditer(pattern, new_line))
                
                for match in reversed(matches):  # Reverse to maintain positions
                    if pattern_type == 'messagebox':
                        # Translate both title and message
                        title = match.group(1)
                        message = match.group(2)
                        
                        if title in TRANSLATIONS:
                            new_title = TRANSLATIONS[title]
                            new_line = new_line[:match.start(1)] + new_title + new_line[match.end(1):]
                            modified = True
                        
                        if message in TRANSLATIONS:
                            new_message = TRANSLATIONS[message]
                            # Adjust position after first replacement
                            message_start = new_line.find(message, match.start(2))
                            if message_start != -1:
                                new_line = new_line[:message_start] + new_message + new_line[message_start + len(message):]
                                modified = True
                    
                    elif pattern_type == 'tab_tuple':
                        # Don't translate the key, only the display text
                        display_text = match.group(2)
                        if display_text in TRANSLATIONS:
                            new_text = TRANSLATIONS[display_text]
                            new_line = new_line[:match.start(2)] + new_text + new_line[match.end(2):]
                            modified = True
                    
                    else:
                        # Single text replacement
                        text = match.group(1)
                        if text in TRANSLATIONS:
                            new_text = TRANSLATIONS[text]
                            new_line = new_line[:match.start(1)] + new_text + new_line[match.end(1):]
                            modified = True
            
            new_lines.append(new_line)
        
        if modified:
            # Backup original
            backup_path = file_path + '.backup'
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
            
            # Write translated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            return True
        
        return False
        
    except Exception as e:
        print(f"Error translating {file_path}: {e}")
        return False

def translate_project(project_root: str = None):
    """Translate entire project safely."""
    if project_root is None:
        project_root = os.getcwd()
    
    # Files to translate
    target_files = [
        'main.py',
        'app/main_window.py',
        'app/tabs/input_tab.py',
        'app/tabs/analysis_tab.py',
        'app/tabs/content_tab.py',
        'app/tabs/prompt_tab.py',
        'app/tabs/prompt_tab_simple.py',
        'app/tabs/settings_tab.py',
        'app/tabs/topic_tab.py',
        'app/tabs/prompt/prompt_generator_ui.py',
        'app/tabs/prompt/prompt_results_panel.py',
        'app/tabs/prompt/prompt_settings_panel.py',
        'app/tabs/prompt/prompt_dialogs.py',
        'app/tabs/prompt/prompt_export_manager.py',
        'utils/ui_components.py',
    ]
    
    # First restore any previous backups
    print("🔄 Khôi phục file gốc từ backup (nếu có)...")
    restore_backups(project_root)
    
    translated_count = 0
    
    print("\n🌏 Bắt đầu dịch giao diện sang tiếng Việt...")
    print(f"📁 Thư mục dự án: {project_root}\n")
    
    for file_path in target_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            if translate_file_safely(full_path):
                print(f"✅ Đã dịch: {file_path}")
                translated_count += 1
            else:
                print(f"⏭️  Bỏ qua: {file_path} (không có text cần dịch)")
        else:
            print(f"❌ Không tìm thấy: {file_path}")
    
    print(f"\n✨ Hoàn tất! Đã dịch {translated_count} files.")
    print("💡 File gốc đã được backup với extension .backup")
    print("🔧 Để khôi phục: python localize_to_vietnamese.py restore")

def restore_backups(project_root: str = None):
    """Restore original files from backups."""
    if project_root is None:
        project_root = os.getcwd()
        
    restored_count = 0
    
    for root, dirs, files in os.walk(project_root):
        # Skip venv and other common directories
        dirs[:] = [d for d in dirs if d not in ['venv', '.git', '__pycache__', '.idea']]
        
        for file in files:
            if file.endswith('.backup'):
                backup_path = os.path.join(root, file)
                original_path = backup_path[:-7]  # Remove .backup
                
                try:
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    with open(original_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Remove backup after restore
                    os.remove(backup_path)
                    
                    rel_path = os.path.relpath(original_path, project_root)
                    print(f"✅ Đã khôi phục: {rel_path}")
                    restored_count += 1
                    
                except Exception as e:
                    print(f"❌ Lỗi khôi phục {original_path}: {e}")
    
    if restored_count > 0:
        print(f"\n✨ Đã khôi phục {restored_count} files về bản gốc.")
    else:
        print("\n📝 Không tìm thấy file backup nào để khôi phục.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'restore':
            # Restore original files
            project_root = sys.argv[2] if len(sys.argv) > 2 else None
            restore_backups(project_root)
        else:
            # Translate project at specified path
            translate_project(sys.argv[1])
    else:
        # Translate project in current directory
        translate_project()
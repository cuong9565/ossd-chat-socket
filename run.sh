# !/bin/bash

# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies và upgrade nếu cần
pip install -r requirement.txt --upgrade
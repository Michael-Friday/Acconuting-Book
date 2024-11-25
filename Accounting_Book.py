import csv #用於處理csv檔案
import matplotlib.pyplot as plt #用於繪製圖表
from matplotlib import rcParams
from matplotlib.front_manager import FontProperties
from datetime import datetime #用於處理和驗證日期
import os
print("當前工作目錄:", os.getcwd())

#設定中文字型
rcParams ['font.sans-serif'] =['SimHei'] #使用黑體
rcParams ['axes.unicode_minus'] = False #避免負號顯示問題

#定義支出檔案名稱
FILE_NAME = "/Users/michael/python/記帳本/Expenses.csv"
'''def read_expenses():
    try:
        with open(FILE_NAME, mode="r", encoding="big5") as file: #指定Big5編碼
            reader = csv.reader(file)
            return list(reader)
    except UnboundLocalError as e: 
        print(f"檔案編碼錯誤: {e}")
        return []
'''

#初始化csv檔案
def initialize_file():
    """檢查檔案存在，若不存在則創建，並寫入標題行"""
    with open(FILE_NAME, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount"])
initialize_file()

#添加支出紀錄
def add_expenses(date, category, amount):
    """讀取所有支出紀錄，返回為字典列表"""
    with open(FILE_NAME, 'a', newline="") as file: #開啟檔案以讀取模式
       writer = csv.writer(file)
       writer.writerow([date, category, amount]) #寫入每一行數據

#讀取支出紀錄
def read_expenses():
    """讀取所有支出距離。返回字典列表"""
    with open(FILE_NAME, 'r') as file: #開啟檔案以讀取模式
        reader = csv.DictReader(file) #將每行讀取為字典
        return list(reader) #返回支出紀錄表


#列出支出紀錄
def list_expenses():
    """在終端機列出所有支出紀錄"""
    expenses = read_expenses() #讀取支出數據
    if not expenses:
        print ("沒有支出紀錄")
        return
    
    print ("\n支出紀錄： ")
    print(f"{'日期':<15}{'類別':<15}{'金額':<10}")
    print ("-" * 40)
    for expense in expenses: #遍歷每筆支出
        print (f"{expense['Date']:<15}{expense['Category']:<15}{expense['Amount']:<10}")
    print()

#繪製支出統計表
def plot_expenses(chart_type = 'pie'):
    """根據類別統計支出，以圓餅圖或和柱狀圖顯示"""  
    expenses = read_expenses() #讀取支出數據
    if not expenses:
        print ("沒有數據可供繪製！") #提示無數據    
        return False
    
    # 彙總那個類別的支出
    categories = {}
    for expenses in expenses:
        category = expenses["Category"] #類別
        amount = float(expenses["Amount"]) #金額轉為浮點小數
        categories[category] = categories.get(category, 0) + amount #總支出

    if chart_type == "pie": #繪製圓餅圖
        plt.figure(figsize=(6,6))
        plt.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=90)
        plt.title("支出類別比例")
    elif chart_type == "bar": #繪製柱狀圖
        plt.figure(figsize=(8, 6))
        plt.bar(categories.keys(), categories.values(), color = "skyblue")
        plt.title("各類別支出金額")
        plt.xlabel("類別")
        plt.ylabel("金額")
    plt.show()

#新增類別
def add_category(category_name):
    """提供新增類別功能"""
    categories = {expenses["Category"] for expenses in read_expenses()} #抓取現有類別集合
    if category_name in categories:
        print(f"類別 '{category_name}' 已存在！")
    else:
        print(f"類別 '{category_name}' 已新增！")

#主介面
def main():
    initialize_file() #確保檔案已經初始化
    while True:
        print("\n === 個人財務助手 === ")
        print("1. 添加支出")
        print("2. 查看支出紀錄表")
        print("3. 繪製支出統計圓餅圖")
        print("4. 繪製支出統計柱狀圖")
        print("5. 新增類別")
        print("6. 離開")

        choice = input("請選擇功能 1-6: ")
        if choice == "1": #添加支出
            data = input ("輸入日期 (YYYY-MM-DD): ")
            try:
                datetime.strptime(data, "%Y-%m-%d") #驗證日期格式
            except ValueError:
                print ("日期格式錯誤，請重新輸入！")
                continue
            category = input("輸入類別（如：食物、交通）： ")
            try:
                amount = float(input("輸入金額: ")) #驗證金額個是
            except ValueError:
                print("金額格式錯誤，請輸入數字！ ")
                continue
            add_expenses(data, category, amount)
            print("支出紀錄已保存!")
        elif choice == "2": #查看支出
            list_expenses()
        elif choice == "3": #圓餅圖
            plot_expenses(chart_type="pie")
        elif choice == "4": #柱狀圖
            plot_expenses(chart_type="bar")
        elif choice == "5": #新增類別
            category_name = input("輸入新增類別名稱: ")
            add_category(category_name)
        elif choice == "6": #離開程式
            print("感謝使用！")
            break
        else: 
            print( "無效的選擇，請重新輸入！")

if __name__ == "__main__":
    main()
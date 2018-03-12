# my_focus_news

用來顯示「感興趣的新聞」的網站。需搭配另一專案 [news_scraper](https://github.com/gn01842919/news_scraper) 使用。


## 頁面功能說明

- Unread News (首頁): 顯示尚未閱讀的感興趣的新聞。
  - 一旦顯示在此頁面，就會被認定為「已讀」，不需要點擊。

- All News: 顯示所有感興趣的新聞。
  - 事實上是顯示資料庫中的所有新聞 (只有感興趣的新聞才會被 [news_scraper](https://github.com/gn01842919/news_scraper) 寫入資料庫)。

- Scraping Rules: 顯示所有用來決定「對哪些新聞感興趣」，以及將新聞分類的規則。
  - 點選其中一個 rule，可看到所有由此 rule 認定為「感興趣」的新聞。
  - 每個 <News, Rule> 組合都會有一個分數，若分數大於零，則該新聞被該 rule 認定為「感興趣」。

- News Categories: 顯示所有新聞分類。
  - 點選其中一個類別，可看到該分類的所有新聞。
  - 一個 Category 可對應到多個 rule，而若某個新聞被顯示在某分類的頁面底下，代表至少有一個該分類對應到的 rule 認定該新聞為「感興趣的」。


## 簡易使用方式

1. 安裝 PostgreSQL。

2. `git clone https://github.com/gn01842919/my_focus_news.git`

3. `git clone https://github.com/gn01842919/news_scraper.git`

4. `pip install -r my_focus_news/requirements.txt`

5. `pip install -r news_scraper/requirements.txt`

6. `python manage.py migrate`

7. `python news_scraper/collect_news_to_db.py`

8. `python manage.py runserver`

9. 瀏覽 http://localhost:8000


## 正式佈署

佈署方式已移至另一專案: [deploy_my_focus_news](https://github.com/gn01842919/deploy_my_focus_news)


## 其他說明

- 此網站開發過程使用 TDD，詳細方法參考自[測試驅動開發：使用 Python (Test-Driven Development with Python)](https://www.tenlong.com.tw/products/9789864760244) 一書。

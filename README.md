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

4. `pip install -r my_focus_news/deployment/requirements.txt`

5. `pip install -r news_scraper/requirements.txt`

6. `python manage.py migrate`

7. `python news_scraper/collect_news_to_db.py`

8. `python manage.py runserver`

9. 瀏覽 http://localhost:8000


## 正式佈署
1. 安裝 Docker 與 Docker Compose

2. `git clone https://github.com/gn01842919/my_focus_news.git`

3. `git clone https://github.com/gn01842919/news_scraper.git`

4. `git clone https://github.com/gn01842919/db_operation_api.git news_scraper/`

5. 依環境與需求調整設定黨，包括:
    1. Django 設定檔 ([my_focus_news/my_focus_news/settings.py](./my_focus_news/settings.py))
    2. news_scraper 設定檔 ([news_scraper/settings.py](https://github.com/gn01842919/news_scraper/blob/master/settings.py))
    3. Docker Compose 設定檔 ([my_focus_news/deployment/docker/docker-compose.yml](./deployment/docker/docker-compose.yml))
    4. [deploy.sh](./deployment/deploy.sh) 中會覆寫上述設定檔的設定(讓開發環境與佈署環境不同)，需要依實際情況調整。目前會/可能被覆寫的設定有:
          1. **Django**: DEBUG, ALLOWED_HOSTS, DATABASES["default"]["PASSWORD"]
          2. **news_scraper**: DATABASE_CONFIG["db_password"], SCRAPER_CONFIG["error_log"]
          3. **docker-compose**: POSTGRES_PASSWORD

6. 執行 `sh my_focus_news/deployment/deploy.sh setup`
    - 此程式會要求使用者輸入資料庫密碼，以及網站 Hostname (用在 Django 的 ALLOWED_HOSTS 設定)，並覆蓋原先設定。
    - 資料庫密碼與 Hostname 可接受空白輸入，會自動抓取環境中的 IP，並使用程式碼中寫死的資料庫密碼。
    - 以下兩項設定無論如何都會被覆寫:
        1. **Django**: DEBUG ==> False
        2. **news_scraper**: ERROR_LOG ==> '/src/scraper_error.log'

7. 測試環境: Ubuntu-16.04

8. TO-DO:
    1. 佈署的位置不要寫死 (目前是 /root)，可再任意路徑執行 deploy.sh，然後會自動下載各個所需的專案，並依環境調整設定。
    2. 若要做到前項所述，deploy.sh 應該獨立出來作為一個專案，不該放在 my_focus_news 裡面。
    3. 做到一個指令就完成所有佈署。


## 其他說明
- 此網站開發過程使用 TDD，詳細方法參考自[測試驅動開發：使用 Python (Test-Driven Development with Python)](https://www.tenlong.com.tw/products/9789864760244) 一書。

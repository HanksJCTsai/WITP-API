# IMP_API
[Python](https://www.python.org/) version 3.7.X

[Django Rest framework](https://www.djangoproject.com/) version (3, 2, 12, 'final', 0)
## Virtual environment by Freeze
```
1.list all package info on old environment
  pip list
2.Pack package to .txt file
   pip freeze > yourname.txt
3.Copy file to new environment
   copy c:\...\...\..(old environment path) c:\...\...\(new environment)
```

## Creat Python Env
```
1.Create a virtual environment to isolate our package dependencies locally
  python -m venv envname
2.Satrt Env (source envname/bin/activate  # On Windows use envname\Scripts\activate)
  python -m pip install --upgrade pip
3.Run Virtual Environment
  envname\Scripts\activate
```

## Install Dependancies
```
1.Enter new environment path and enter python cmd
  python
2.Install package by version file yourname.txtx
  pip install -r <yourname_requirements>
3.list and check install result
   pip list
```
## 第一種情況：最初即使用現有的資料庫
	1. 在settings.py修改要連線的資料庫。
	2. 執行python manage.py inspectdb可以產生資料庫模型，把它複製貼到models.py。
class Quiz(models.Model):
    question_text = models.CharField(max_length=200)
class Meta:
        managed = True
        app_label = 'quiz'
        db_table = 'preexist'
	4. 執行下面語句：
python manage.py makemigrations quiz
接著執行：
python manage.py migrate quiz
結果報錯：
django.db.utils.ProgrammingError: relation "preexist" already exists
如果直接跑runserver，結果會出現：
You have 1 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): quiz.
Run 'python manage.py migrate' to apply them.
改用fake再跑runserver就沒有跑出上面的問題了，就可以繼續進行專案。
python manage.py migrate --fake quiz
第二種情況：中途轉換資料庫
一、保留migrations下的記錄
假設中途想改用另外的資料庫，欄位跟現在的資料庫不相同，資料模型就必須修改。
資料庫設定跟資料模型修改好，執行基本步驟後，跟上個情況報一樣的錯：
django.db.utils.ProgrammingError: relation "quiz_question" already exists
同樣跑fake後執行runserver沒問題。
二、刪除migrations下的記錄
	1. 讓整個執行紀錄回到零：
python manage.py migrate --fake quiz zero
結果跑出：
Operations to perform:
  Unapply all migrations: quiz
Running migrations:
  Rendering model states... DONE
  Unapplying animal.0001_initial... FAKED
2.接著就可以手動刪除migrations底下的檔案，除了__init__.py。
3.重新建立資料紀錄檔：
python manage.py makemigrations quiz
結果：
    Migrations for 'quiz':
  quiz/migrations/0001_initial.py
    - Create model Choice
	4. 因為是現有的資料庫，必然不能直接執行migrate，所以要用fake：
python manage.py migrate --fake-initial quiz
結果：
Operations to perform:
  Apply all migrations: quiz
Running migrations:
  Applying animal.0001_initial... FAKED
這樣就不會動到現有的資料又可以更改資料庫模型了！
fake vs fake--initial
就今天試做的感覺，兩者在這兩種情況都可以解決報錯的問題，差別在於initial的方法，讓我們可以刪除多餘的migrations紀錄，畢竟整個資料庫都重置，先前的紀錄檔案也沒有留下的必要。

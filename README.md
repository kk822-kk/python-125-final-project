# Geo-Pop — სოციალური ქსელი
სრულფასოვანი სოციალური ქსელი, შექმნილი Django 6.0.5-ზე სასწავლო ფინალური პროექტისტვის.



ფუნქციონალი

- ავტორიზაცია — რეგისტრაცია, შესვლა, გამოსვლა (პროფილის ფოტოთი)
- პოსტები (CRUD) — ტექსტური და ფოტო პოსტების შექმნა, ნახვა, რედაქტირება, წაშლა
- ინტერაქცია — Like, კომენტარი, გაზიარება
- ძებნა — მომხმარებლების პოვნა Username-ით
- მეგობრების სისტემა — დამატება და სიის ნახვა პროფილზე



ტექნოლოგიები

|   Back-End   |   Front-End   | სხვა |
|--------------|---------------|------|
|  Python 3.x  |  HTML5 / CSS3 | SQLite |
| Django 6.0.5 |  Bootstrap 5  | Git & GitHub |
|  Django ORM  |   JavaScript  | Pillow |



ინსტალაცია და გაშვება

1. კლონირება
git clone https://github.com/kk822-kk/python-125-final-project.git
cd python-125-final-project

2. ვირტუალური გარემოს შექმნა
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate


3. დამოკიდებულებების დაყენება
pip install -r requirements.txt


4. მიგრაციები და სერვერის გაშვება
python manage.py migrate
python manage.py runserver


5. ბრაუზერში გახსნა
http://127.0.0.1:8000
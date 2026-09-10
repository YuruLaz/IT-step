# FastAPI HTTP Methods Demo

FastAPI აპლიკაცია, სადაც `/products` ენდპოინტზე დამუშავებულია GET, POST, PUT, PATCH და DELETE
მოთხოვნები. Request body საჭირო არ არის — თითოეული ენდპოინტი მხოლოდ დემონსტრაციისთვის აბრუნებს
შესაბამის შეტყობინებას.

## გაშვება

```bash
cd homework/Lesson_37
pip install -r requirements.txt
uvicorn main:app --reload
```

შემდეგ გახსენით http://127.0.0.1:8000/docs, სადაც ინტერაქტიულად შეგიძლიათ ყველა ენდპოინტის
გამოცდა.

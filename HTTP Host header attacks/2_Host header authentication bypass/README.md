# Host header authentication bypass
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-authentication-bypass

## Phân tích
- Bắt gói `GET /` vào Repeater, đổi Host header sang 1 host khác xem thử có access homepage ko. Ta thấy vẫn get 200 OK
![img.png](img.png)
- Access vào file `robots.txt` xem có gì hay ho ko. Ta thấy có /admin panel nhưng đã bị chặn
![img_1.png](img_1.png)

![img_2.png](img_2.png)

- Ta thấy chỉ local users mới access đc

## Resolve lab

- Thay Host với localhost, mục đích để đánh lừa server là request được gởi từ máy local. Ta thấy có thể thấy đc path để xóa user
![img_3.png](img_3.png)

![img_4.png](img_4.png)
- User đã đc xóa (gói 302)

![img_5.png](img_5.png)
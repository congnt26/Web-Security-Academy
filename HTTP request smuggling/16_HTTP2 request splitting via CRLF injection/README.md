# HTTP/2 request splitting via CRLF injection
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-request-splitting-via-crlf-injection

## Phân tích
- Check xem HTTP/2 work
![img.png](img.png)
- Add 1 smuggle req như bên dưới
![img_1.png](img_1.png)
- Gởi normal req
![img_2.png](img_2.png)
- Ok, đã inject thành công
- Giờ ta mong muốn là bắt gói 200/302 từ victim user để lấy cookie, để detect nhanh gói 302 thì ta sửa cho attack req luôn là 404 để khi 1 victim req gởi đến, ta sẽ nhận đc 302 ngay lập tức

## Resolve lab
- Sửa path thay vì /, dùng /404a. Send...
![img_3.png](img_3.png)
- Note: send vài lần để bắt 302 (thậm chí là many times !_! )
![img_4.png](img_4.png)
- Dùng cookie của admin để login và xóa carlos
![img_5.png](img_5.png)
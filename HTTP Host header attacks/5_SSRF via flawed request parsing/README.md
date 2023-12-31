# SSRF via flawed request parsing
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-ssrf-via-flawed-request-parsing

## Phân tích
- Gởi `GET /` request vào Repeater, thay Host bằng 1 invalid domain, hay localhost hay Burp collaborator ... đều thấy Forbidden.
![img.png](img.png)
- Nhận thấy ta có thể truy cập trang web với 1 absolute URL cho GET req
![img_1.png](img_1.png)
- Thay Host bằng domain khác, ta thấy timeout thay vì Forbidden, điều này chứng tỏ server đang validate absolute URL thay vì Host header.
![img_2.png](img_2.png)
- Ta xác nhận Host header attack bằng cách thay nó bằng Burp collaborator --> có response, quay lại bài 4 trước đó.
![img_3.png](img_3.png)
- Ta intruder private ip này, bài này ip là 192.168.0.88
![img_4.png](img_4.png)
- Gởi request sang Repeater, check `GET /admin` xem
![img_5.png](img_5.png)

## Resolve lab
- Change Request method từ GET sang POST request với csrf token và username bên dưới
![img_6.png](img_6.png)
- Resolved
![img_7.png](img_7.png)
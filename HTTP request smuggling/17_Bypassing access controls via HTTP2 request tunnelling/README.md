# Bypassing access controls via HTTP/2 request tunnelling
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-bypass-access-controls-via-request-tunnelling

## Phân tích
- Nhận thấy rằng request ko work với các HTTP/1.1 smuggle thông thường
![img.png](img.png)
- Xác định HTTP/2 ở FE.
  - Bật Allow HTTP/2 ALPN override:
    - Giải thích: Enabling this setting allows you to send HTTP/2 requests from Burp Repeater even when the server doesn't advertise HTTP/2 support via ALPN. This lets you explore any "hidden HTTP/2" attack surface reported by Burp Scanner or manually test for hidden HTTP/2 support.
    - Mục đích để chắc chắn là HTTP/2 chạy

  ![img_1.png](img_1.png)
  - Send
  ![img_2.png](img_2.png)
- Xác định CRLF cho HTTP/2. Tạo mới 1 header với Host địa chỉ khác
![img_3.png](img_3.png)
- Ta thấy host abc.com đã đc inject xuống BE, nghĩa là CRLF work
- Tiếp theo, tìm cách Leak các internal headers dùng CRLF injection
  - Dùng diagram sau
  ![img_5.png](img_5.png)
  - Sử dụng search function, vì nó hiển thị giá trị trả về ngay trên web ui
  ![img_4.png](img_4.png)
  - Update lại request header để inject 1 search vào
  ![img_7.png](img_7.png)
  - Tăng giá trị CL lên để xem hết các internal headers
  ![img_8.png](img_8.png)
  - Now, what do we do with the headers? It would seem these headers indicate certificate authentication is in play. Let’s look at the key/value pairs and see what we can do.
    - X-SSL-VERIFIED: 0 – if ‘0’ means unverified, ‘1’ probably means verified
    - X-SSL-CLIENT-CN: null – if CN stands for Common Name as is typical with certs, we know that we need to login with the administrator account per error message when attempting to access the ‘/admin’ page.
    - X-FRONTEND-KEY: <LONG NUMBER> – not really sure what this one does at this point. Seems unrelated to the certificate auth and is most likely just an identifier the backend uses to ensure it is talking to a trusted frontend.
- Smuggle a request to the admin page
  - Dùng diagram sau
  ![img_9.png](img_9.png)
  - Cách này là ta lồng 1 smuggle request đến `GET /admin` bên trong 1 normal request là `GET /`
  ![img_10.png](img_10.png)
  - Thực tế vẫn ko thấy được trang admin vì response nó chưa toàn bộ data của home page (/) rồi.
  - Ta có thể workaround bằng cách thay vì dùng GET, ta dùng HEAD
  ![img_11.png](img_11.png)
  - HEAD của home page có CL là 8363
  ![img_12.png](img_12.png)
  - Điều này nghĩa là CL của /admin (sau khi đã authen) nó chỉ 3608, trong CL trong request header là 8363
  - Ta phải thử 1 path khác sao cho CL ~3600 để thấy toàn bộ nội dung của /admin
  - Thử với /admin
  ![img_13.png](img_13.png)
  ![img_14.png](img_14.png)
  - Vẫn không thấy được các path cần thiết để xóa user
  - Thử với /login (đối với lab này thì CL: 3247, cũng gần bằng 3600)
  ![img_15.png](img_15.png)
  - Đã thấy path delete
  
  ![img_16.png](img_16.png)
  - Send, ta thấy response sau, 500ISE do ko thỏa điều kiện của CL, ko sao, do đây là blind attack nên GET request để xóa user đã thực hiện.
  
  ![img_18.png](img_18.png)
  - Check lab resolve ok.

![img_17.png](img_17.png)
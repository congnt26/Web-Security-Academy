# Host validation bypass via connection state attack
https://portswigger.net/web-security/host-header/exploiting/lab-host-header-host-validation-bypass-via-connection-state-attack

## Phân tích
- Ý tưởng bài này là tận dụng việc reuse HTTP connection để exploit
- Nhận gói `GET /` đổi Host header, nó luôn trả về 301 Moved Permanently
![img.png](img.png)
- Ví dụ trên cho ta thấy server luôn xác thực cho request đầu tiên mà server nhận được qua một kết nối mới.
- Ta có thể bypass bằng cách gởi 2 request 1 lúc trong cùng 1 connection, request đầu tiên thì bình thường, nhưng request thứ 2 là tới 1 exploit system
- Tạo 1 normal req
![img_1.png](img_1.png)
- Attack req 
![img_2.png](img_2.png)
- Gởi cùng 1 lúc với Group: single-connection, check attack response
![img_3.png](img_3.png)
- Thêm /admin vào check thử
![img_4.png](img_4.png)

## Resolve lab
- Làm tương tự như bài trước, chuyển sang POST, thêm csrf và username
![img_5.png](img_5.png)
- Solved !!
![img_6.png](img_6.png)
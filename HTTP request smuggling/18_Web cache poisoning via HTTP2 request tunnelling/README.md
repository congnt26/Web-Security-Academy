# Web cache poisoning via HTTP/2 request tunnelling
https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-web-cache-poisoning-via-request-tunnelling

# Phân tích
- Confirm CRLF
  - Thêm :path header vào với invalid source, expect để thấy 404
  - OK, new path đã override path cũ (/)
![img.png](img.png)
  - Có thể inject CRLF vào
![img_1.png](img_1.png)
  - Thử smuggle 1 request trong path, đây là muốn hiển thị 404 trong response
![img_2.png](img_2.png)
  - Thực tế ko hiển thị 404, response toàn là home page
- Chuyển qua HEAD --> Turn blind into non-blind using HEAD
  - Send và nhận timeout
  ![img_3.png](img_3.png)
  - Vì CL của homepage là 8520, trong khi nội dung của page cần hiển thị (404) là 11 thôi, nên ko đủ để hiển thị
  ![img_4.png](img_4.png)
  - Nên là phải tìm  1 page có CL ít nhất phải >=8520 để nội dung đó hiển thị lên
    - Có thể tìm trong các bài post
    ![img_7.png](img_7.png)
    - Sửa lại `/post?postId=10`
    ![img_8.png](img_8.png)
- Find a sink for a reflection attack
  - Pick any request /resource.../xxx.js
  ![img_9.png](img_9.png)
  - Add alert
  ![img_10.png](img_10.png)
  - Add vào smuggle request
  ![img_11.png](img_11.png)
  - Timeout vì CL ko đủ
  - Add padding bằng cách tạo 1 payload với 10k bytes
  ![img_12.png](img_12.png)
  - Gởi lại xem có append vào ko
  ![img_13.png](img_13.png)
  - Ok, add payload vào smuggle
  ![img_14.png](img_14.png)
  - Access vào /?cachebuster=1
  ![img_15.png](img_15.png)
  ![img_16.png](img_16.png)
  - Chuyển lại `GET /`
  ![img_17.png](img_17.png)
  - Access homepage, ta thấy page luôn hiện HTTP/1.1 302..., điều này do cache
  - Chuyển qua 1 url khác, vd: /cachebuster2 , ta thấy lab resolve

![img_18.png](img_18.png)
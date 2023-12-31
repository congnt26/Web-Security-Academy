# Client-Side Desync
https://portswigger.net/web-security/request-smuggling/browser/client-side-desync/lab-client-side-desync

## Phân tích

- Dùng diagram dưới để detect
![img.png](img.png)
- Check homepage, ta thấy 302 redirect tới `/en`
![img_1.png](img_1.png)
- Check với HTTP/2 xem có work ko bằng cách upgrade to HTTP/2
![img_2.png](img_2.png)
- Thấy error, check Allow HTTP/2 ALPN override, send, ta thấy Stream failed --> ko chạy đc với HTTP/2, back về HTTP/1.1
![img_3.png](img_3.png)
- Gởi 1 request sau (nhớ tắt update Content-Length trong request repeater)
![img_4.png](img_4.png)
  - Specify CL=20 để trả về timeout vì ko có body request
  - Ta thấy server response 200 OK
  - Đúng là phải timeout --> detect client-side desync (CSD)
- Xác nhận CSD
  - Send attack
  ![img_5.png](img_5.png)
  - Check normal res
  ![img_6.png](img_6.png)
- Confirm client-side desync in the Browser (thêm Connection: keep-alive trong attack req, group attack+normal với Single connection)
  - Attack req
  ![img_7.png](img_7.png)
  - Normal req
  ![img_8.png](img_8.png)
  ==> yes, confirm CSD work
- Nãy giờ là ta dùng trên Burp để xác nhận CSD, giờ ta dùng web để xem thực tế CSD có chạy ko
  - Tạo 1 file js như sau, idea là làm lại những gì làm ở burp bao gồm cả attack + normal req
  ![img_10.png](img_10.png)
  - Chạy trên chrome console (nhớ tắt Burp proxy)
  ![img_9.png](img_9.png)
  ![img_11.png](img_11.png)
  - Ta thấy có 404 not found --> ok
- Identify an exploitable gadget
  - Add thử 1 comment trong blog, gởi vào burp
  ![img_12.png](img_12.png)
  - Smuggle post comment req trong attack req
  ![img_14.png](img_14.png)
  - Lưu ý CL: 400 vì ta muốn thấy các nội dung của response victim sẽ append vào trong comment
  ![img_13.png](img_13.png)
  - Smuggling thành công
  ![img_15.png](img_15.png)
- Confirm the vulnerable gadget in the browser
  - Tạo js để smuggle post comment thay vì GET /404
  ![img_16.png](img_16.png)
  
  ```
  fetch("https://0a0a00b20453f9b38034a88e00eb00fe.h1-web-security-academy.net/",{
  method:"POST",
  body: "POST /en/post/comment HTTP/1.1\r\nHost: 0a0a00b20453f9b38034a88e00eb00fe.h1-web-security-academy.net\r\nCookie: session=74fSjPcaajbmV0BluUhymsQEWAqQzkK4\r\nContent-Length: 400\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\ncsrf=0PExVl7oweyN5w3pWRQucVZ6ldiBivSY&postId=5&name=cong&email=cong%40gmail.com&website=&comment=test4",
  credentials: "include", //ensure we use the 'with-cookie' connectio pool
  mode: "cors", //will show an error, ensure we dont follow 302 redirect
  }).catch(() => {
  fetch("https://0a0a00b20453f9b38034a88e00eb00fe.h1-web-security-academy.net/en", {
  credentials: "include",
  mode: "no-cors", //won't trigger the error
  });
  });
  ```
  
  - On console:
  ![img_18.png](img_18.png)
  ![img_19.png](img_19.png)
  ![img_20.png](img_20.png)
  - Craft exploit server (nhớ add script tag)
  ![img_21.png](img_21.png)
  - Deliver to victim
  ![img_22.png](img_22.png)
  - Ta thấy response của victim đã in trên comment nhưng ko thấy session cookie vì CL ko đủ để hiển thị
  - Vào exploit server, Tăng CL lên (400 --> 900), check comment
  ![img_23.png](img_23.png)
  - Login with session id đó (dùng Cookie-editor extension của Chrome)
  ![img_24.png](img_24.png)
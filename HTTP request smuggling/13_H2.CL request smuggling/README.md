# H2.CL request smuggling
https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-cl-request-smuggling

## Phân tích

- Thử downgrade HTTP/1.1 và thêm `Transfer-Encoding: chunked` --> not work --> request ko support chunk --> dùng HTTP2
![img.png](img.png)
- Thử sumggle HTTP2
  - Attack req
![img_1.png](img_1.png)
  - Normal req --> 404 Not found
![img_2.png](img_2.png)
==> request smuggling như sau: append request thứ 2 vào prefix của request smuggling. GET tới 1 resource ko thấy nên trả về 404
![img_3.png](img_3.png)

- Note: thỉnh thoảng thấy sau khi gởi normal req thì vẫn trả 200 OK, là do server tự động gởi GET request in background (hãy hiểu như là giả lập 1 số user khác họ access tới web đó, trên thực tế thì 1 server ko thể chỉ mỗi chúng ta access mà còn những user khác). 
  - Do đó, gởi thử vài lần attack-normal-attack-normal.... để coi 404 Not found.

- Để resolve lab, ta phải redirect đến 1 exploit server. Thử coi `GET /resources/js` request
![img_4.png](img_4.png)
![img_5.png](img_5.png)

<a id='a1'></a>
- Smuggle request này 
![img_6.png](img_6.png)
![img_8.png](img_8.png)
- Ta thấy location ko phải là abc.com như mong muốn, thử đổi smuggle request
![img_9.png](img_9.png)
![img_10.png](img_10.png)

- Ok, giờ chỉnh sửa trên exploit server
![img_11.png](img_11.png)

## Resolve lab

- Gởi attack req như sau
![img_12.png](img_12.png)
- Normal req
![img_13.png](img_13.png)
- Ta thấy 302, cũng đúng, nhưng lab này mong muốn là victim user (1 user khác ngoài chúng ta, ở đây là các GET request của chính server gởi đến - dạng giả lập)
- Do đó 302 phải phải đc nhận từ victim user (để victim họ redirect sang 1 exploit server), và mong muốn normal req của chúng ta phải là 200 OK
- Gởi atk-nor-atk-nor... cho đến khi normal req là 200 OK, check xem lab resolve chưa 
- Vẫn chưa resolve, bởi vì victim nó buộc phải request tới file javascript để nó redirect tới exploit server, nhưng có trường hợp cái [smuggle của ta ở trên](#a1) nó append vào 1 file khác nên lab vẫn chưa resolve. Ví dụ:
![img_14.png](img_14.png)
- Check log của exploit server xem có log của victim request tới file js này ko
![img_15.png](img_15.png)


![img_16.png](img_16.png)

## Cách khác dùng Intruder
- Gởi Smuggle request qua induder, run Snipper với payload null = 100 (run 100 lần). Resource pool là 1 với delay 100ms
- Check 2 response 200OK liên tiếp, check xem lab resolve chưa
![img_17.png](img_17.png)

![img_18.png](img_18.png)
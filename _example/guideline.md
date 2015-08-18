---
# 新页面向导
layout: page
permalink: "page.html" # 页面地址，请修改
title:  "页面标题" # 页面标题，请修改
---

这里使用 Markdown 语法即可，你不会不知道[什么是 Markdown](http://daringfireball.net/projects/markdown/) 吧。

然后下面列举一些在这里特殊的使用方式：

{% highlight html %}
<p>这里就是一段代码区域，在这里的代码会自动高亮，你可以替换 html 成其他的语言。</p>
{% endhighlight %}

```
<p>这里就是一段代码区域，在这里的代码不会自动高亮</p>
```

`这是行内代码，如果你想让你的代码不分成额外的段落，请使用它。`

请注意，如果出现英文单词或者数字，请在两侧额外空格（如果那一侧有标点，那么可以不空格），如果是中英文混合词汇，可以不用空格（比如`b站`）。

文章中标点符号请尽量使用全角标点，比如逗号、句号、括号（单/双引号请使用半角，并做好空格，例如：` “` 和 `” `）。

你可以 [Fork 这个项目](https://github.com/fuckbilibili/fuckbilibili.github.io/fork)，复制这个文件（`/_example/guideline.md`）到 `/articles/` 目录下，重新命名文件名，删掉这些向导，修改标题和页面地址，并写一篇文章。你只需要 Commit 之后发起 Pull request，通过审核后，你的文章就可以发表了。

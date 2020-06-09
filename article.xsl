<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/article">

    <html>
      <head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="provider" content="m.cnki.net" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0, minimum-scale=1.0, maximum-scale=1.0" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black" />
    <meta name="format-detection" content="telephone=no" />
        <title>
          <xsl:value-of select="title"/>
        </title>
        <link rel="stylesheet" type="text/css" href="/mcnki/css/article.css"/>
      </head>

      <body>
<!-- The Modal -->
<div id="myModal" class="modal">

  <!-- The Close Button -->
  <span class="close">&#215;</span>

  <div class="modal-wrap">
  <!-- Modal Content (The Image) -->
  <img class="modal-content" id="img01"/>
  </div>
  <!-- Modal Caption (Image Text) -->
  <div id="caption"></div>
</div>
        <header class="comhead">
          <a href="javascript:history.go(-1)" class="leftreturn"> 返回</a>
          
          <!--<span class="optbox">
            <a href="javascript:void(0)" title="更多" class="commore"> 更多</a>
          </span>-->
          <span class="optbox" >
            <a href="javascript:void(0)" onclick="showMenu()" title="更多" class="commore" id="commore"> 更多</a>
          </span>
         
          
        </header>
        <div class="sidenav">
          <dl class="sidenav-list" id="mainMenu" style="display:none;">
            <dt class="tit">目录</dt>
            <!--<ul class="mainMenu" id="mainMenu" style="display:none;">-->
            <xsl:for-each select="body/section">
              <xsl:variable name="myid" select="@id"/>
              <xsl:for-each select="node()">
                <xsl:choose>
                  <xsl:when test="name()='title'">
                    <dd class="guide noico">
                      <p>
                        <a>
                          <xsl:attribute name="href">
                            <xsl:text>#</xsl:text>
                            <xsl:value-of select="$myid"/>
                          </xsl:attribute>
                          <span>
                            <xsl:value-of select="current()"/>
                          </span>

                        </a>
                      </p>
                    </dd>
                  </xsl:when>

                  <xsl:when test="name()='subsection'">
                    <xsl:variable name="myid1" select="@id"/>
                    <ul class="contentbox">
                      <xsl:for-each select="node()">
                        <xsl:choose>
                          <xsl:when test="name()='title'">
                            <li>
                              <a>
                                <xsl:attribute name="href">
                                  <xsl:text>#</xsl:text>
                                  <xsl:value-of select="$myid1"/>
                                </xsl:attribute>
                                <span>
                                  <xsl:value-of select="current()"/>
                                </span>

                              </a>

                            </li>
                          </xsl:when>
                        </xsl:choose>
                      </xsl:for-each>
                    </ul>
                  </xsl:when>
                </xsl:choose>
              </xsl:for-each>
            </xsl:for-each>
            <!--<li>
              <a href="/mcnki" title="中国知网首页">
                <img src="/mcnki/images/menu01.png"/>
                <span>首页</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/User/GuanZhu/kuaibao">
                <img src="/mcnki/images/menu07.png"/>
                <span>我的图书馆</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/literature/search" title="文献检索">
                <img src="/mcnki/images/menu06.png"/>
                <span>文献检索</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/Publication/Search" title="出版物">
                <img src="/mcnki/images/menu05.png"/>
                <span>出版物</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/LiteratureSeniorSearch" title="高级检索">
                <img src="/mcnki/images/menu03.png"/>
                <span>高级检索</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/XueKeMenu.do" title="学科分类">
                <img src="/mcnki/images/menu04.png"/>
                <span>学科分类</span>
              </a>
            </li>
            <li>
              <a href="/mcnki/User/Detail" title="cnki">
                <img src="/mcnki/images/menu02.png"/>
                <span>我的CNKI</span>
              </a>
            </li>-->
            <!--</ul>-->
          </dl>
        </div>
        <div class="article_body" onclick="">
          <div class="article_title_cn">
            <xsl:value-of select="title[string-length(@xml:lang) &lt; 1]"/>
          </div>
          <div class="article_author_cn">
            <xsl:for-each select="prolog/authormeta/authorinformation">
              <h class="article_author_i">
                <xsl:value-of select="personinfo/namedetails/fullname"/>
                <xsl:if test="position()!=last()">, </xsl:if>
              </h>
            </xsl:for-each>
          </div>
          <xsl:apply-templates select="abstract[string-length(@xml:lang) &lt; 1]"/>
          <xsl:if test="prolog/metadata/keywords[string-length(@xml:lang) &lt; 1]/keyword">
            <div class="article_keywords_cn">
              <b>关键词：</b>
              <xsl:for-each select="prolog/metadata/keywords[string-length(@xml:lang) &lt; 1]/keyword">
                <h class="article_author_i">
                  <xsl:value-of select="current()"/>
                </h>
              </xsl:for-each>
            </div>
          </xsl:if>
          <!--正文开始-->
          <xsl:for-each select="body">
            <xsl:for-each select="node()">
              <xsl:choose>
                <xsl:when test="name()='section'">
                  <xsl:apply-templates select="current()"/>
                </xsl:when>
                <xsl:when test="name()='p'">
                  <p>
                    <xsl:for-each select="node()">
                      <xsl:choose>
                        <xsl:when test="name()='sup'">
                          <sup>
                            <xsl:value-of select="current()"/>
                          </sup>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:value-of select="current()"/>
                        </xsl:otherwise>
                      </xsl:choose>
                    </xsl:for-each>
                  </p>
                </xsl:when>
                <xsl:when test="name()='figure'">
                  <p>
                    <img class="width" onclick="swipe(this);">
                      <xsl:attribute name="src">
                        <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                        <xsl:value-of select="current()/image/@href"/>
                      </xsl:attribute>
                    </img>
                  </p>
                </xsl:when>
                <xsl:when test="name()='image'">
                  <p>
                    <img class="width" onclick="swipe(this);">
                      <xsl:attribute name="src">
                        <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                        <xsl:value-of select="current()/@href"/>
                      </xsl:attribute>
                    </img>
                  </p>
                </xsl:when>
                <xsl:when test="name()='subsection'">
                  <xsl:apply-templates select="current()"/>

                </xsl:when>
              </xsl:choose>
            </xsl:for-each>
          </xsl:for-each>

          <!--正文结束-->
          <!--参考文献开始-->
          <div class="article_reference">
            <xsl:if test="bibliography/biblioitem">
              <div class="reference_title">参考文献</div>
              <ul class="reference_list">
                <xsl:for-each select="bibliography/biblioitem">
                  <li>
                    <div class="article_en">
                      <xsl:value-of select="title"/>
                    </div>
                  </li>
                </xsl:for-each>
              </ul>
            </xsl:if>
          </div>
          <!--参考文献结束-->
          <!--英文信息-->
          <div>
            <div class="article_title_en">
              <xsl:value-of select="title[@xml:lang='en']"/>
            </div>
            <div class="article_author_en">
              <xsl:for-each select="prolog/authormeta/authorinformation">
                <h class="article_author_i">
                  <xsl:value-of select="personinfo/namedetails/fullname[@xml:lang='en']"/>
                  <xsl:if test="position()!=last()">, </xsl:if>
                </h>
              </xsl:for-each>
            </div>
            <xsl:apply-templates select="abstract[@xml:lang='en']"/>
          </div>
          <xsl:if test="prolog/metadata/keywords[@xml:lang='en']/keyword">
            <div class="article_keywords_en">
              <b>Keywords：</b>
              <xsl:for-each select="prolog/metadata/keywords[@xml:lang='en']/keyword">
                <h class="article_author_i">
                  <xsl:value-of select="current()"/>
                  <xsl:if test="position()!=last()">, </xsl:if>
                </h>
              </xsl:for-each>
            </div>
          </xsl:if>
          <!--作者简介-->
          <div class="author_intro_title">
            <xsl:value-of select="authorintro"/>
          </div>
        </div>
</body>
<script type="text/javascript">
    var prevTarget=null;
    function swipe(el) {
    // Get the modal
    var modal = document.getElementById('myModal');

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var img = el;//document.getElementById('myImg');
    var modalImg = document.getElementById("img01");
    var captionText = document.getElementById("caption");

    modal.style.display = "block";
    modalImg.src = img.src;
    captionText.innerHTML = img.alt;
    var span = document.getElementsByClassName("close")[0];
    span.onclick = function () {
    modal.style.display = "none";
    }
    };

    function showMenu(){
    <!--$("#mainMenu").toggle();-->

    if ( document.getElementById("mainMenu").style.display==="block")
    document.getElementById("mainMenu").style.display="none";
    else {
    document.getElementById("mainMenu").style.display="block";
    addClickEventListener();
    }
    };


    function addClickEventListener() {
    document.addEventListener('click', capture_mouseup);
    };
    function removeClickEventListener() {
    document.removeEventListener('click', capture_mouseup);
    };
    function capture_mouseup(e) {
    prevTarget = e.target;
    if (prevTarget === null || prevTarget.id !='commore') {
    document.getElementById("mainMenu").style.display="none";
    removeClickEventListener();
    }
    };
  </script>
    </html>
  </xsl:template>

  <!--章节-->
  <xsl:template match="section">
    <xsl:variable name="myid" select="@id"/>
    <xsl:for-each select="node()">
      <xsl:choose>
        <xsl:when test="name()='title'">
          <div class="section_title">
            <xsl:attribute name="id">
              <xsl:value-of select="$myid"/>
            </xsl:attribute>
            <xsl:value-of select="current()"/>
          </div>
        </xsl:when>
        <xsl:when test="name()='p'">
          <p>
            <xsl:for-each select="node()">
              <xsl:choose>
                <xsl:when test="name()='sup'">
                  <sup>
                    <xsl:value-of select="current()"/>
                  </sup>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="current()"/>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:for-each>
          </p>
        </xsl:when>
        <xsl:when test="name()='figure'">
          <p>
            <img class="width" onclick="swipe(this);">
              <xsl:attribute name="src">
                <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                <xsl:value-of select="current()/image/@href"/>
              </xsl:attribute>
            </img>
          </p>
        </xsl:when>
        <xsl:when test="name()='image'">
          <p>
            <img class="width" onclick="swipe(this);">
              <xsl:attribute name="src">
                <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                <xsl:value-of select="current()/@href"/>
              </xsl:attribute>
            </img>
          </p>
        </xsl:when>
        <xsl:when test="name()='subsection'">
          <xsl:apply-templates select="current()"/>

        </xsl:when>
      </xsl:choose>
    </xsl:for-each>
    </xsl:template>
  <!--章节1-->
  <xsl:template match="subsection">
    <xsl:variable name="Position" select="count(../preceding-sibling::*[name()!='section'])+1"/>
    <xsl:variable name="myid" select="@id"/>
    <xsl:for-each select="node()">
      <xsl:choose>
        <xsl:when test="name()='title'">
          <xsl:choose>
            <xsl:when test="$Position=1">
              <div class="subsection_title">
                <xsl:attribute name="id">
                  <xsl:value-of select="$myid"/>
                </xsl:attribute>
                <xsl:value-of select="current()"/>
              </div>
            </xsl:when>
            <xsl:when test="$Position=2">
              <div class="threesection_title">
                <xsl:attribute name="id">
                  <xsl:value-of select="$myid"/>
                </xsl:attribute>
                <xsl:value-of select="current()"/>
              </div>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="current()"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <xsl:when test="name()='p'">
          <p>
            <xsl:for-each select="node()">

              <xsl:choose>
                <xsl:when test="name()='sup'">
                  <sup>
                    <xsl:value-of select="current()"/>
                  </sup>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="current()"/>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:for-each>
          </p>
        </xsl:when>
        <xsl:when test="name()='figure'">
	<p>
            <img class="width" onclick="swipe(this);">
              <xsl:attribute name="src">
                <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                <xsl:value-of select="current()/image/@href"/>
              </xsl:attribute>
            </img>
          </p>
        </xsl:when>
        <xsl:when test="name()='image'">
          <p>
            <img class="width" onclick="swipe(this);">
              <xsl:attribute name="src">
                <xsl:text>http://oaokms.cnki.net/resource/static/</xsl:text>
                <xsl:value-of select="current()/@href"/>
              </xsl:attribute>
            </img>
          </p>
        </xsl:when>
        <xsl:when test="name()='subsection'">
          <xsl:apply-templates select="current()"/>

        </xsl:when>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="abstract">
    <xsl:choose>
      <xsl:when test="@xml:lang='en'">
        <div class="article_abstract_en">
          <b>Abstract：</b>
          <xsl:value-of select="current()"/>
        </div>
      </xsl:when>
      <xsl:otherwise>
        <div class="article_abstract_cn">
          <b>摘要：</b>
          <xsl:value-of select="current()"/>
        </div>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="getFatherPosition">
    <xsl:variable name="Position" select="count(../preceding-sibling::*[name()!='section'])+1"/>
    <xsl:value-of select="$Position"/>
  </xsl:template>
</xsl:stylesheet>

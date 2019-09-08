<html>
	<head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <title>{{title}}</title>
        <link href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
        <script src="https://cdn.bootcss.com/d3/5.9.7/d3.min.js"></script>
    </head>
    <body>
        <div class="form-inline">
        <textarea id="input_text" style="min-width: 40%" class="form-control" rows="4">俄罗斯对意大利应美国要求拘留俄罗斯公民感到愤怒。”美国司法部5日宣称，57岁的俄罗斯“间谍”科尔舒诺夫和59岁的意大利“间谍”比安齐因涉嫌窃取美国通用电气航空集团商业机密在意大利那不勒斯机场被拘留。对此，俄罗斯总统普京及俄外交部对意大利此举表示强烈不满，并警告称这种行为是不公平竞争的一个例子，将损害两国关系。</textarea>
        <button type="button" class="btn btn-primary" onclick="sendNews2Server()">Extract=></button>
        </div>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th >人物</th>
                    <th>观点</th>
                </tr>
            </thead>
            <tbody id="summaries">
            </tbody>
        </table>

        <script>
            function sendNews2Server(){
                console.info($("#input_text").val())
                $("#summaries").html("");
                $.ajax({
                    type: 'POST',
                    url: '/automaton/summary',
                    data: $("#input_text").val(),
                    dataType: 'json',
                    success: function (data){
                        console.info(data)
                        let html="";
                        for(let idx=0;idx<data.summary.length;++idx){
                            const frag = "<tr><td>"+data.summary[idx].speaker+"</td><td>"+data.summary[idx].content+"</td></tr>";
                            html+=frag;
                        }
                        $("#summaries").html(html);
                    },
                    error: function () {

                    }
                })
            };
        </script>
    </body>
</html>
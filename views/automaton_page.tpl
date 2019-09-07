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
        <textarea id="input_text" style="min-width: 40%" class="form-control" rows="4"></textarea>
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
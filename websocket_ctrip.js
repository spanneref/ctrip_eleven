var ws = require("nodejs-websocket");
console.log("开始建立连接...")

var cached = {

}
var server = ws.createServer(function(conn){
    conn.on("text", function (msg) {
        if (!msg) return;
        // conn.sendText(str)
        // console.log(str);
        if (msg.length > 1000){
            console.log("接受到js代码...")
        }else{
            console.log("errmsg: %s" % msg);
        }
        var key = conn.key;
        if ((msg === "Browser") || (msg === "Python")){
            // browser或者python第一次连接
            cached[msg] = key;
            console.log("cached",cached);
            return;
        }
        console.log(cached, key);
        if (Object.values(cached).includes(key)){
            console.log(server.connections.forEach(conn=>conn.key));
            var targetConn = server.connections.filter(function(conn){
                return conn.key !== key;
            })
            console.log(targetConn.key);
            console.log("正在发送js代码...");
            targetConn.forEach(conn=>{
                conn.send(msg);
            })
        }
        // broadcast(server, str);
    })
    conn.on("close", function (code, reason) {
        console.log("关闭连接")
    });
    conn.on("error", function (code, reason) {
        console.log("异常关闭")
    });
}).listen(8080)
console.log("WebSocket建立完毕")


// var server = http.createServer(function(request, response){
//     response.end("ok");
// }).listen(8000);
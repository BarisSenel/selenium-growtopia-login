server = HttpServer.new()

server:setLogger(function(request, response)
    print(string.format("Method: %s, Path: %s, Status: %i", request.method, request.path, response.status))
end)

server:post("/addGmailBot",function(request,response)
    local token = request:getParam("token")
    addBot(token)
    response:setContent("Bot token added with " .. token, "text/plain")
end)

server:listen("0.0.0.0", 80)

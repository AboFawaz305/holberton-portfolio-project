import serverFactory from 'spa-server'

var server = serverFactory.create({
  path: './dist/',
  port: 5173,
  fallback: '/index.html',
})

server.start()

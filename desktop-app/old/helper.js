function errWithStack(err) {
  stack = new Error().stack
  console.log(stack + '\\' + err)
}

module.exports = {
  errWithStack: errWithStack
}

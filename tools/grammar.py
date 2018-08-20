Grammar = [{
  "name": "Expr",
  "rules": {
    "Ternary": ["Token operator", "Expr conditional", "Expr left", "Expr right"],
    "Binary": ["Expr left", "Token operator", "Expr right"],
    "Grouping" : ["Expr expression"],
    "Literal"  : ["Object value"],
    "Unary"    : ["Token operator", "Expr right"]
  }
}]

from flask import Flask
app = Flask("Market bot")
# import flask_table
@app.route("/")
def hello_world():
    tableofgood = """
     <table>
  <tr>
    <td>Emil</td>
    <td>Tobias</td>
    <td>Linus</td>
  </tr>
  <tr>
    <td>16</td>
    <td>14</td>
    <td>10</td>
  </tr>
</table> 
    """
    return "<p>hi </p>"


@app.route("/hello")
def hello_world1():
    tableofgood = """
     <table>
  <tr>
    <td>Emil</td>
    <td>Tobias</td>
    <td>Linus</td>
  </tr>
  <tr>
    <td>16</td>
    <td>14</td>
    <td>10</td>
  </tr>
</table> 
    """
    return tableofgood


if __name__ == '__main__':

    print("hello")
    app.run()



from flask import Flask ,render_template
app=Flask(__name__)
@app.route("/")
def html():
    return render_template("html.html")
    return render_template()
if __name__=='__main__':
    app.run(debug=True)

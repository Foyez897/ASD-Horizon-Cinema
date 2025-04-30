from views.index import IndexView

if __name__ == "__main__":
    app = IndexView()
    app.mainloop()
    import os
os.environ["TK_SILENCE_DEPRECATION"] = "1"
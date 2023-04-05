def initialize_style():
    global style
    style = """
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 2px;
            background: white;
            border-radius : 1px;
        }
        
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #5c5c5c;
            width: 10px;
            margin-bottom : -7px;
            margin-top : -7px;
            border-radius: 5px;
            }
            
        QSlider::sub-page:qlineargradient {
            background: gray;
            background-color : #3167D1;
        }
        
        QPushButton{
            border : none;
            border-radius : 5px;
            padding : 2px;
            background-color : white;
        }
    
    """


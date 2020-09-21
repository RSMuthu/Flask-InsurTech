from .auth import Login, Register, Logout
from .company import Company_Create, All_Company, Trigger_mail
from .messages import Text_Msg
from .general_routes import Form_Entry, Msg_Board, DashBoard, Index_Login

def initialise_routes (api):
    '''
    initialises all the routes/endpoints defined

    api - Flask_RESTful API is sent as input for adding the resources
    '''
    api.add_resource(Login, '/auth/signin', endpoint="login")
    api.add_resource(Register, '/auth/signup', endpoint="register")
    api.add_resource(Logout, "/auth/signout", endpoint="logout")
    api.add_resource(Company_Create, "/company", endpoint="company")
    api.add_resource(Form_Entry, "/company/fill_form/<cipher_id>", endpoint="form")
    api.add_resource(Msg_Board, "/company/msg_board/<cipher_id>", endpoint="msg_board")
    api.add_resource(All_Company, "/company/all", endpoint="all_com")
    api.add_resource(Text_Msg, "/company/msg/<c_id>", endpoint="company_msgs")
    api.add_resource(Trigger_mail, "/company/mail_to_contact/<c_id>", endpoint="email")
    api.add_resource(DashBoard, "/dashboard", endpoint="dashboard")
    api.add_resource(Index_Login, "/", endpoint="index")

    #__add_route_for_peek(api)

def __add_route_for_peek(api):
    '''
    seperate mapping for the data peeping endpoints.
    thus this can be commented out after troubleshoot.
    --> for timesake, not using DEBUG/DEV/PROD modes for discriminating test endpoints

    api - Flask_RESTful API is sent as input for adding the resources
    '''
    from .god_view import User_view, Company_view, Message_view
    api.add_resource(User_view, "/try/peeking/users")
    api.add_resource(Company_view, "/try/peeking/companies")
    api.add_resource(Message_view, "/try/peeking/msgs")

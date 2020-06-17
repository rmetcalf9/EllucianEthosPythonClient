# Base class for login sessions

class LoginSession():
  def injectHeaders(self, headers):
    raise Exception("LoginSession.injectHeaders Not Implemented")

  # Return true if sucessful and falst if not
  #  true will prompt the APIClient to resend the request
  def refresh(self):
    raise Exception("LoginSession.refresh Not Implemented")

class NullLoginSession():
  def injectHeaders(self, headers):
    return

  def refresh(self):
    return False #no session to refresh so no need to retry call
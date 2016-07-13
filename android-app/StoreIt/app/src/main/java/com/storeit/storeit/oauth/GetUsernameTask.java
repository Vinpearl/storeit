package com.storeit.storeit.oauth;

import android.app.Activity;
import android.os.AsyncTask;
import android.util.Log;
import com.google.android.gms.auth.GoogleAuthException;
import com.google.android.gms.auth.GoogleAuthUtil;
import com.google.android.gms.auth.UserRecoverableAuthException;
import com.storeit.storeit.activities.LoginActivity;

import java.io.IOException;

/**
 * Created by loulo on 10/05/2016.
 */
public class GetUsernameTask extends AsyncTask<Void, Void, Void> {
    Activity mActivity;
    String mScope;
    String mEmail;

    public GetUsernameTask(Activity activity, String name, String scope) {
        this.mActivity = activity;
        this.mScope = scope;
        this.mEmail = name;
    }

    /**
     * Executes the asynchronous job. This runs when you call execute()
     * on the AsyncTask instance.
     */
    @Override
    protected Void doInBackground(Void... params) {
        try {
            String token = fetchToken();
            if (token != null) {
                Log.v("GetUsernameTask", "token : " + token);

                LoginActivity activity = (LoginActivity)mActivity;
                activity.tokenReceived(token);

            }
        } catch (IOException e) {
        }
        return null;
    }

    /**
     * Gets an authentication token from Google and handles any
     * GoogleAuthException that may occur.
     */
    protected String fetchToken() throws IOException {
        try {
            return GoogleAuthUtil.getToken(mActivity, mEmail, mScope);
        } catch (UserRecoverableAuthException userRecoverableException) {


            LoginActivity activity = (LoginActivity)mActivity;
            activity.handleException(userRecoverableException);
            
//            Log.e("GetUsernameTask", userRecoverableException.getMessage());

        } catch (GoogleAuthException fatalException) {
        }
        return null;
    }
}
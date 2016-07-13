package com.storeit.storeit.activities;

import android.os.Bundle;
import android.preference.ListPreference;
import android.preference.PreferenceActivity;
import android.preference.PreferenceFragment;

import com.storeit.storeit.R;

import java.io.File;
import java.util.ArrayList;

/**
 * Created by loulo on 16/06/2016.
 */
public class StoreItPreferences extends PreferenceActivity {

    static File[] mSavePath;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mSavePath = getExternalFilesDirs(null);

        getFragmentManager().beginTransaction().replace(android.R.id.content, new MyPreferenceFragment()).commit();
    }

    public static class MyPreferenceFragment extends PreferenceFragment {
        @Override
        public void onCreate(final Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            addPreferencesFromResource(R.xml.preferences);

            ListPreference lp = (ListPreference) findPreference("pref_key_storage_location");

            ArrayList<CharSequence> entryValues = new ArrayList<>();

            for (File f : mSavePath) {
                entryValues.add(f.getPath());
            }
            lp.setEntries(entryValues.toArray(new CharSequence[entryValues.size()]));
            lp.setEntryValues(entryValues.toArray(new CharSequence[entryValues.size()]));
        }
    }
}

/*
  SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(getBaseContext());
  String strUserName = SP.getString("username", "NA");
  boolean bAppUpdates = SP.getBoolean("applicationUpdates",false);
  String downloadType = SP.getString("downloadType","1");
*/
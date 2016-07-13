package com.storeit.storeit.adapters;

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;
import com.storeit.storeit.R;

/**
 * Adapter for the recycleview of the main activity
 * Is used for the main menu
 * Each item have one text and one image
 */
public class MainAdapter extends RecyclerView.Adapter<MainAdapter.ViewHolder> {

    private static final int TYPE_HEADER = 0;  // Header
    private static final int TYPE_ITEM = 1; // Item du menu

    private String mNavTitles[]; // item title
    private int mIcons[];       // item icon

    // Profil header
    private String name;        //String Resource for header View Name
    private int profile;        //
    private String email;       //String Resource for header view email
    Context context;

    public static class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {
        int Holderid;

        TextView textView;
        ImageView imageView;
        ImageView profile;
        TextView Name;
        TextView email;
        Context contxt;

        public ViewHolder(View itemView,int ViewType,Context c) {
            super(itemView);
            contxt = c;
            itemView.setClickable(true);
            itemView.setOnClickListener(this);

            // Menu item
            if(ViewType == TYPE_ITEM) {
                textView = (TextView) itemView.findViewById(R.id.rowText);
                imageView = (ImageView) itemView.findViewById(R.id.rowIcon);
                Holderid = 1;
            }
            else{ // Profil header


                Name = (TextView) itemView.findViewById(R.id.name);
                email = (TextView) itemView.findViewById(R.id.email);
                profile = (ImageView) itemView.findViewById(R.id.circleView);
                Holderid = 0;
            }
        }


        @Override
        public void onClick(View v) {
        }
    }

    public MainAdapter(String Titles[], int Icons[], String Name, String Email, int Profile, Context passedContext){
        mNavTitles = Titles;
        mIcons = Icons;
        name = Name;
        email = Email;
        profile = Profile;
        this.context = passedContext;

    }

    @Override
    public MainAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {

        if (viewType == TYPE_ITEM) {
            View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_row,parent,false);
            return new ViewHolder(v,viewType,context);
        } else if (viewType == TYPE_HEADER) {
            View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.header,parent,false);
            return new ViewHolder(v,viewType,context);
        }
        return null;
    }

    @Override
    public void onBindViewHolder(MainAdapter.ViewHolder holder, int position) {
        if(holder.Holderid ==1) {
            holder.textView.setText(mNavTitles[position - 1]);
            holder.imageView.setImageResource(mIcons[position -1]);
        }
        else{

            holder.profile.setImageResource(profile);
            holder.Name.setText(name);
            holder.email.setText(email);
        }
    }

    // Number of items in the list
    @Override
    public int getItemCount() {
        return mNavTitles.length+1; // + 1 for the header
    }

    @Override
    public int getItemViewType(int position) {
        if (isPositionHeader(position))
            return TYPE_HEADER;
        return TYPE_ITEM;
    }

    private boolean isPositionHeader(int position) {
        return position == 0;
    } // header is first
}
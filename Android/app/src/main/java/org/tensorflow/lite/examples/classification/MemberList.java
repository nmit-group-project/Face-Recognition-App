package org.tensorflow.lite.examples.classification;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.List;

public class MemberList extends ArrayAdapter<Member>
{
    private Activity context;
    private List<Member> list;

    public MemberList(Activity context,List<Member> list)
    {
        super(context,R.layout.user_info, list);
        this.context = context;
        this.list=list;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent)
    {
        LayoutInflater inflater=context.getLayoutInflater();
        View view=inflater.inflate(R.layout.user_info,null,true);

        TextView name=(TextView) view.findViewById(R.id.user);
        Member member=list.get(position);

        name.setText(member.getName());
        return view;
    }
}
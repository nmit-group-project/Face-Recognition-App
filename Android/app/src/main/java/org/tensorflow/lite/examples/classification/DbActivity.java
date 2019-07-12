package org.tensorflow.lite.examples.classification;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ListView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


import java.util.ArrayList;
import java.util.List;

public class DbActivity extends AppCompatActivity
{
    ListView ListView;
    DatabaseReference reference;
    List<Member> memberList;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_db);

        reference=FirebaseDatabase.getInstance().getReference("Member");
        ListView=(ListView) findViewById(R.id.Listview);
        memberList=new ArrayList<>();
    }

    @Override
    protected void onStart()
    {
        super.onStart();

        reference.addValueEventListener(new ValueEventListener()
        {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot)
            {
                memberList.clear();
                for(DataSnapshot ds:dataSnapshot.getChildren())
                {
                    Member member=ds.getValue(Member.class);
                    memberList.add(member);
                }
                MemberList adapter=new MemberList(DbActivity.this,memberList);
                ListView.setAdapter(adapter);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError)
            {
            }
        });
    }
}
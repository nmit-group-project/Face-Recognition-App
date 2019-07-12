package org.tensorflow.lite.examples.classification;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.tensorflow.lite.examples.classification.tflite.Classifier;

public class AttendActivity extends AppCompatActivity
{

    DatabaseReference reference;
    public TextView name;
    Member member;
    public String msg;
    public Button button;
    long maxid=0;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_attend);
        name=findViewById(R.id.name);
        button=findViewById(R.id.button);
        Bundle bundle=getIntent().getExtras();
        msg=bundle.getString("attend");
        name.setText(msg);

        reference= FirebaseDatabase.getInstance().getReference().child("Member");
        member = new Member();
        reference.addValueEventListener(new ValueEventListener()
        {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot)
            {
                if(dataSnapshot.exists())
                {
                    maxid=(dataSnapshot.getChildrenCount());
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError)
            {

            }
        });
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                member.setName(name.getText().toString().trim());
                reference.push().setValue(member);
                Toast.makeText(AttendActivity.this, ""+msg+" marked present", Toast.LENGTH_SHORT).show();
                Intent intent=new Intent(AttendActivity.this,ClassifierActivity.class);
                startActivity(intent);
            }
        });

    }
    public void again(View view)
    {
        Intent intent=new Intent(this,ClassifierActivity.class);
        startActivity(intent);
    }
}
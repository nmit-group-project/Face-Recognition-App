package org.tensorflow.lite.examples.classification;

public class Member
{
   String name;

   public  Member(String name)
   {
      this.name = name;
   }

   public  Member()
   {
   }
   public String getName()
   {
       return name;
   }

   public void setName(String name)
   {
       this.name = name;
   }
}

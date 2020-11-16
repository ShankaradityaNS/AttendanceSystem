import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:firebase_database/ui/firebase_animated_list.dart';
import 'package:flutter/material.dart';

class CustomData extends StatefulWidget {
  CustomData({this.app});
  final FirebaseApp app;
  @override
  _CustomDataState createState() => _CustomDataState();
}

class _CustomDataState extends State<CustomData> {
  final referenceDatase = FirebaseDatabase.instance;
  final studentsName = 'Student"s Name';
  final student = TextEditingController();

  DatabaseReference _stdRef;
  @override
  void initState(){
    final FirebaseDatabase database = FirebaseDatabase(app: widget.app);
        _stdRef= database.reference().child('Students');

        super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final ref = referenceDatase.reference();
    return Scaffold(
      appBar: AppBar(
        title: Text('List of students'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
          Center(
            child: Container(
              color: Colors.green,
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height,
              child: Column(
                children: [
                  Text(
                      studentsName,
                      textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold ) ,
                  ),
                  TextField(
                    controller: student,
                    textAlign: TextAlign.center,
                  ),
                  FlatButton(
                      color: Colors.grey,
                      onPressed: (){
                    ref
                    .child('Students')
                        .push()
                        .child(studentsName)
                        .set(student.text)
                        .asStream();
                    student.clear();
                  },child: Text('Save data'),
                    textColor: Colors.white,
                  ),
                  Flexible(
                      child: new FirebaseAnimatedList(
                        shrinkWrap: true,
                      query: _stdRef, itemBuilder: (BuildContext context,
                  DataSnapshot snapshot,
                  Animation<double> animation,
                  int index){
                        return new ListTile(
                        trailing: IconButton(icon: Icon(Icons.delete),onPressed: () =>
                          _stdRef.child(snapshot.key).remove(),),
                          title: new Text(snapshot.value['StudentsTitle']),
                        );
                  })),
                ],
    ),
    ),
    ),
        ],

      ),
      ),
    );
  }
}

use std::process::Command;
use std::{thread, time};
use serde_json::Value;
use std::fs::File;
use std::io::{Read, Write};
use clap::{Arg, Command as ClapCommand};

fn main() {
    let cmd = ClapCommand::new("MyApp")
        .version("1.0")
        .arg(
            Arg::new("file_name")
                .long("file_name")  
                .value_name("file_name")
                .default_value("metadata.json")
        )
        .arg(
            Arg::new("mode")
                .long("mode")
                .value_name("mode")
                .default_value("sidecar")
        )
        .get_matches();

  let file_name = cmd.get_one::<String>("file_name").unwrap().as_str();
  let mode = cmd.get_one::<String>("mode").unwrap().as_str();
  let mut files: Vec<(String, String)> = Vec::new();
  
  // iterate from 100 to 5000 with step 100
    for mut i in (0..500).step_by(500) {
        if i == 0 {
            i = 100;
        }
        let ret = run_test(file_name, mode, &i.to_string());
        // push the file name and the destination name
        files.push((ret.0, ret.1));
    }

  let ten_secs = time::Duration::from_secs(21);
  thread::sleep(ten_secs);

  files.iter().for_each(|(name, des)| {
    cp_file(name, des);
  });
}


fn run_test(file_name: &str, mode: &str, qps: &str) -> (String, String) {
    let mut file = File::open(file_name).expect("Failed to open file");
    let mut contents = String::new();
    file.read_to_string(&mut contents).expect("Failed to read file");
    let mut data: Value = serde_json::from_str(&contents).expect("Failed to parse JSON");
    data["metadata"]["qps"] = Value::String(qps.to_string());
    

    let new_contents = serde_json::to_string(&data).expect("Failed to serialize JSON");
    let mut new_file = File::create(file_name).expect("Failed to create file");
    new_file.write_all(new_contents.as_bytes()).expect("Failed to write file");


    let url = format!(r#"fortio curl -stdclient -payload-file {} "http://localhost/client/fortio/rest/run?jsonPath=.metadata""#, file_name);    
    let output = Command::new("sh")
                         .arg("-c")
                         .arg(url)
                         .output()
                         .expect("Failed to execute command");
    
    // Convert the output bytes to a string
    let result = String::from_utf8_lossy(&output.stdout);
    let val: Value = serde_json::from_str(&result).expect("Failed to parse JSON");
    let id = val["RunID"].as_u64().unwrap();

    let url = format!(r#"curl  "http://localhost/client/fortio/rest/status?runid={}""#, id);
    let output = Command::new("sh")
                         .arg("-c")
                         .arg(url)
                         .output()
                         .expect("Failed to execute command");
    let result = String::from_utf8_lossy(&output.stdout);
    let val: Value = serde_json::from_str(&result).expect("Failed to parse JSON");
    let id = val["Statuses"][id.to_string().as_str()]["RunnerOptions"]["ID"].as_str().unwrap();
    let name = format!("{}.json",id);
    let des = format!("{}_{}.json",qps,mode);

    (name, des)
}


fn cp_file(name: &str, des: &str) {
    let url = format!(r#"kubectl cp `kubectl get pod -l app=fortio-client -o jsonpath='{{.items[0].metadata.name}}'`:{} {}"#,name, des);
    Command::new("sh")
                         .arg("-c")
                         .arg(url)
                         .output()
                         .expect("Failed to execute command");
}
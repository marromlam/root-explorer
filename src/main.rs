use std::pin::Pin;

use std::path::Path;
use failure::Error;
use futures::{Stream, StreamExt};
use nom::number::complete::*;

use root_io::{core::parsers::string, stream_zip, tree_reader::Tree, RootFile};

/// A model for the (or a subset) of the data.
/// This is the object which contains the data of one "event"
#[derive(Debug)]
#[allow(dead_code)]
struct Model {
    one: i32,
    two: f32,
    three: String,
}

impl Model {
    fn stream_from_tree(t: Tree) -> Result<Pin<Box<dyn Stream<Item = Self>>>, Error> {
        Ok(stream_zip!(
            t.branch_by_name("one")?
                .as_fixed_size_iterator(|i| be_i32(i)),
            t.branch_by_name("two")?
                .as_fixed_size_iterator(|i| be_f32(i)),
            t.branch_by_name("three")?
                .as_fixed_size_iterator(|i| string(i))
        )
        .map(|(one, two, three)| Self { one, two, three })
        .boxed_local())
    }
}

async fn read_simple(f: RootFile) {

    println!("ola bro");
    let t = f.items()[0].as_tree().await.unwrap();
    let s = Model::stream_from_tree(t).unwrap();
    s.for_each(|m| async move {
        println!("{:?}", m);
    })
    .await
}


#[tokio::main]
async fn main() -> Result<(), std::io::Error> {
// fn main() -> Result<(), failure::Error> {
    async fn read_simple_local() {
        let path = Path::new("./src/test_data/simple.root");
        let f = RootFile::new(path).await.expect("Failed to open file");
        read_simple(f).await;
    }
    let _ = read_simple_local();
    println!("ola bro");
        let path = Path::new("/Users/marcos/Projects/work/phis-scq.git/sidecar/2015/MC_Bs2JpsiPhi/v0r5.root");
        let f = RootFile::new(path).await.expect("Failed to open file");
        // let f = RootFile::new(path);
        let t = f.items(); //[0].as_tree().await.unwrap();
        // let t =  f.items()[0].as_tree().unwrap();
        println!("{:?}", t[0].as_tree().await.unwrap());

    Ok(())
}

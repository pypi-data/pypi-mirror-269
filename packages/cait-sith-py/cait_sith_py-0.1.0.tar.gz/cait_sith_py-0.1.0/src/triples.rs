use std::sync::{Arc, Mutex};

use cait_sith::protocol::Action;
use cait_sith::protocol::{MessageData, Participant, Protocol};
use cait_sith::triples::{TripleGenerationOutput, TriplePub, TripleShare};
use k256::Secp256k1;
use pyo3::prelude::*;
use pyo3::{pyclass, pyfunction, PyResult};

use crate::{
    create_action_enum, create_protocol, participant::convert_participants,
    participant::PyParticipant,
};

#[pyclass(name = "TripleShare")]
#[derive(Clone, Debug)]
pub struct PyTripleShare {
    #[pyo3(get)]
    pub a: String,
    #[pyo3(get)]
    pub b: String,
    #[pyo3(get)]
    pub c: String,
}

impl From<TripleShare<Secp256k1>> for PyTripleShare {
    fn from(value: TripleShare<Secp256k1>) -> Self {
        Self {
            a: serde_json::to_string(&value.a).unwrap(),
            b: serde_json::to_string(&value.b).unwrap(),
            c: serde_json::to_string(&value.c).unwrap(),
        }
    }
}

impl From<PyTripleShare> for TripleShare<Secp256k1> {
    fn from(value: PyTripleShare) -> Self {
        Self {
            a: serde_json::from_str(&value.a).unwrap(),
            b: serde_json::from_str(&value.b).unwrap(),
            c: serde_json::from_str(&value.c).unwrap(),
        }
    }
}

#[pyclass(name = "TriplePublic")]
#[derive(Clone, Debug)]
pub struct PyTriplePublic {
    #[pyo3(get)]
    pub big_a: String,
    #[pyo3(get)]
    pub big_b: String,
    #[pyo3(get)]
    pub big_c: String,

    /// The participants in generating this triple.
    #[pyo3(get)]
    pub participants: Vec<PyParticipant>,
    /// The threshold which will be able to reconstruct it.
    #[pyo3(get)]
    pub threshold: usize,
}

impl From<TriplePub<Secp256k1>> for PyTriplePublic {
    fn from(value: TriplePub<Secp256k1>) -> Self {
        Self {
            big_a: serde_json::to_string(&value.big_a).unwrap(),
            big_b: serde_json::to_string(&value.big_b).unwrap(),
            big_c: serde_json::to_string(&value.big_c).unwrap(),
            participants: convert_participants(value.participants),
            threshold: value.threshold,
        }
    }
}

impl From<PyTriplePublic> for TriplePub<Secp256k1> {
    fn from(value: PyTriplePublic) -> Self {
        Self {
            big_a: serde_json::from_str(&value.big_a).unwrap(),
            big_b: serde_json::from_str(&value.big_b).unwrap(),
            big_c: serde_json::from_str(&value.big_c).unwrap(),
            participants: convert_participants(value.participants),
            threshold: value.threshold,
        }
    }
}

#[pyclass(name = "TripleGenerationOutput")]
#[derive(Debug, Clone)]
pub struct PyTripleGenerationOutput {
    #[pyo3(get)]
    pub share: PyTripleShare,
    #[pyo3(get)]
    pub public: PyTriplePublic,
}

impl From<TripleGenerationOutput<Secp256k1>> for PyTripleGenerationOutput {
    fn from(value: TripleGenerationOutput<Secp256k1>) -> Self {
        Self {
            share: value.0.into(),
            public: value.1.into(),
        }
    }
}

impl From<PyTripleGenerationOutput> for TripleGenerationOutput<Secp256k1> {
    fn from(value: PyTripleGenerationOutput) -> Self {
        (value.share.into(), value.public.into())
    }
}

create_action_enum!(
    TripleGenerationAction,
    TripleGenerationOutput<Secp256k1>,
    PyTripleGenerationOutput
);

create_protocol!(
    TripleGenerationProtocol,
    TripleGenerationOutput<Secp256k1>,
    TripleGenerationAction
);

/// Generate a triple through a multi-party protocol.
///
/// This requires a setup phase to have been conducted with these parties
/// previously.
///
/// The resulting triple will be threshold shared, according to the threshold
/// provided to this function.
#[pyfunction(name = "generate_triple")]
pub fn py_generate_triple(
    participants: Vec<PyParticipant>,
    me: PyParticipant,
    threshold: usize,
) -> PyResult<TripleGenerationProtocol> {
    let participants: Vec<Participant> = convert_participants(participants);
    let me = me.into();
    let protocol =
        cait_sith::triples::generate_triple(participants.as_slice(), me, threshold)
            .map_err(|err| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", err)))?;
    let wrapped = Arc::new(Mutex::new(protocol));
    Ok(TripleGenerationProtocol { protocol: wrapped })
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterController : MonoBehaviour
{
    private Animator Anim;
    private CharacterController Frank;
    private float timeToChangeDirection;
    // Start is called before the first frame update
    void Start()
    {
        Anim = GetComponent<Animator>();
        Frank = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        timeToChangeDirection -= Time.deltaTime;
        
        if (timeToChangeDirection <= 0)
        {
            ChangeDirection();
        }

    }
    private void ChangeDirection()
    {
        float angle = Random.Range(0f, 360f);
        Quaternion quat = Quaternion.AngleAxis(angle, Vector3.up);
        Vector3 newRotation = quat * Vector3.left;
        transform.Rotate(newRotation);
        timeToChangeDirection = Random.Range(1f, 4f);
        Debug.Log(timeToChangeDirection);
        Anim.SetBool("walk", true);
        
    }
}
